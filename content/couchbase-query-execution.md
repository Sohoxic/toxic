---
title: "Parallel operators at the bottom, blocking operators at the top: Couchbase Query Internals, part 1"
template: light-theme.html
---

![Parallel operators fan out at the bottom of the plan into N workers; a single blocking operator merges, sorts and limits at the top before rows go out.](/assets/images/query-internals-1-cover.png)

## What one line of a package doc comment taught me about data parallelism

I was reading through the `execution` package the other day and hit [the doc comment at the top of `execution/execution.go`](https://github.com/couchbase/query/blob/master/execution/execution.go#L9-L13):

> Package execution provides query execution. The execution is data-parallel to the extent possible.

Two sentences. I nodded and kept scrolling, then stopped and admitted I didn't actually know what either one meant.

The rabbit hole that followed cost me an afternoon, mostly on things I assumed I already understood. Here's where I came out: the engine parallelizes the wide, cheap, per-document work at the bottom of the plan, then funnels into serial operators at the top, where the data has already been reduced to something small. That's what the comment is hedging about. The engine wants maximum data parallelism; query semantics put a ceiling on it.

If you already knew that, you can stop here. If it sounds like a sentence you'd nod at without being able to defend, that was me last Tuesday, and the rest is the working out.

## Execution is the third act

A query goes through three stages before you get rows back. First it gets parsed, so `SELECT name FROM users WHERE age > 30` becomes a syntax tree. Then it gets planned, which is where the engine decides *how* to answer it: which index to use, what order to join things in, whether it can push a predicate down. The output of planning is a tree of operators.

The `execution` package is the third stage. It takes that tree and actually runs it.

## Operators are just small workers

An operator is one step. It has one job. `IndexScan` produces document keys. `Fetch` turns keys into actual documents. `Filter` throws out rows that fail the `WHERE`. `Project` reshapes what's left into the columns you asked for.

Strung together, they look like a Unix pipeline:

```
IndexScan → Fetch → Filter → Project → client
```

The thing that clicked for me is that each operator is genuinely ignorant of the others. `Filter` does not know or care whether its rows came from an index scan or a full scan. It reads from an input channel, applies a predicate, writes to an output channel, done. That's the whole contract.

I wrote a toy version to convince myself:

```go
type Row map[string]interface{}

type FilterOperator struct {
    Predicate func(Row) bool
}

func (f *FilterOperator) Run(input <-chan Row, output chan<- Row) {
    defer close(output)
    for row := range input {
        if f.Predicate(row) {
            output <- row
        }
    }
}
```

Two things in there tripped me up as a Go beginner, so briefly:

`map[string]interface{}` is a dictionary with string keys and values of any type. It looks sloppy until you remember we're dealing with JSON documents that have no fixed schema. One document might have an `age` field, the next one might not, and a third might have it as a string. A rigid struct can't hold that. The real engine uses a proper `value.Value` type instead of a bare map, but the reason it exists is the same.

The arrows in `<-chan Row` and `chan<- Row` are direction markers. The first says "this function can only receive from this channel," the second says "can only send." It's the compiler stopping you from accidentally writing to your own input.

## Pipeline parallelism is free

Each operator runs in its own goroutine, and channels connect them. That already buys you something: `Fetch` doesn't wait for `IndexScan` to finish. The moment the first key pops out, `Fetch` starts working on it while `IndexScan` keeps going.

This is why you get first results back quickly on a big query instead of staring at nothing until the whole scan completes.

But that's not what "data-parallel" means.

## Data parallelism is the other axis

Pipeline parallelism is different workers doing *different jobs*. Data parallelism is many workers doing the *same job* on *different data*.

If you have 10,000 documents that all need `age > 30` evaluated, one goroutine chewing through them sequentially is a waste of a machine with eight cores. So the engine clones the operator N times and lets all N read from the same input channel:

```go
for i := 0; i < N; i++ {
    go func() {
        for row := range input {
            if row["age"].(int) > 30 {
                output <- row
            }
        }
    }()
}
```

This is the bit that surprised me. I assumed splitting work across goroutines needed some kind of dispatcher deciding who gets what. It doesn't. Multiple goroutines can all range over the same channel, and Go delivers each value to exactly one of them. Whichever worker is free grabs the next row. The channel *is* the work queue. No locks, no manual partitioning, no coordination code.

The reason this works for `Filter` and needs no extra machinery is that there's no shared state. Worker 2 doesn't need to know what Worker 1 decided. Checking whether document #5 passes the predicate requires zero information about document #4. Every decision is self-contained.

### It's an operator, not a special case

What I liked when I went looking for the real thing: the engine doesn't scatter this fan-out logic across every operator that wants it. There's a single operator called `Parallel` whose entire job is to be a container. It wraps a child sub-plan, makes N copies of it, and points every copy at the same input and the same output:

```go
func (this *Parallel) runChild(child Operator, context *Context, parent value.Value) {
    child.SetInput(this.input)
    child.SetOutput(this.output)
    child.SetParent(this)
    child.SetStop(nil)
    this.fork(child, context, parent)
}
```

That's my toy loop, wearing a suit. Same input channel handed to every clone, same output channel collected from every clone, and `fork` doing the `go` part. The child has no idea it's been cloned. `Filter` doesn't contain a single line of parallelism-aware code — it just gets copied and handed a channel that happens to have four other readers on it.

So when the planner wants a stage parallelized, it doesn't reach for a parallel version of that operator. It wraps the ordinary one in `Parallel`. Composition rather than special-casing, which is why adding a new operator doesn't mean writing a concurrent variant of it too.

### Where N comes from

N isn't a constant. It's negotiated:

```go
n := util.MinInt(this.plan.MaxParallelism(), context.MaxParallelism())
```

One side is what the *plan* thinks this stage can usefully absorb, the other is what the *request context* permits — which traces back to the node's `max-parallelism` setting and the per-request `max_parallelism` parameter. The smaller number wins. It's a nice detail: the planner proposes, the runtime caps, and you can dial an individual query down without touching the cluster.

Worth noting these two forms of parallelism multiply rather than compete. Every stage already has its own goroutine (pipelining), and now some of those stages are N goroutines wide (data parallelism). A four-stage plan with N=4 on two of the stages isn't running four things at once, it's running ten.

One consequence of the fan-out: output order is not input order. Workers finish at different speeds, so rows come out scrambled. For a filter that's fine. Hold that thought.

## "To the extent possible" is doing a lot of work

Now the second half of the comment. Not every operator has that convenient independence.

Try to fan out `GROUP BY city, COUNT(*)` the same way and you immediately have a problem:

```go
counts := map[string]int{}

for i := 0; i < N; i++ {
    go func() {
        for doc := range docs {
            counts[doc.City]++   // several goroutines, one map, very bad
        }
    }()
}
```

Go maps aren't safe for concurrent writes. Two goroutines bumping `counts["Paris"]` at the same instant will corrupt it or panic outright.

The fix is nicer than adding a mutex. Give every worker its own private map. No sharing means no race, and no lock contention either:

```go
func groupWorker(docs <-chan Doc, result chan<- map[string]int) {
    local := map[string]int{}
    for doc := range docs {
        local[doc.City]++
    }
    result <- local
}
```

Each worker ends up with a partial answer that's correct for the slice of data it happened to see, and wrong as a global total, because Paris documents got scattered across several workers. So one goroutine at the end sums the partials together.

That merge step is serial, and that's fine. You're adding up eight small maps, not re-reading a million documents. The expensive part was parallel; the cheap part didn't need to be.

The same reasoning explains the other blocking operators. `ORDER BY` can't know the globally-first row until every row has arrived. `LIMIT 10` is meaningless per-shard. `DISTINCT` can't spot duplicates that landed on different workers. All of these have to funnel through a single point.

Which is why a query like this:

```sql
SELECT city, COUNT(*)
FROM airport
WHERE country = "France"
GROUP BY city
ORDER BY COUNT(*) DESC
LIMIT 5;
```

is wide and parallel at the bottom (scan, fetch, filter, partial grouping) and narrow and serial at the top (merge, sort, limit). By the time data reaches the serial part it's been reduced to something small enough that the serialization doesn't hurt.

That's the shape the comment was describing. Parallelize aggressively where the data is big and the work is independent. Accept a single-threaded funnel where the semantics demand it.

## The bit I'll actually remember

Two sentences of doc comment turned out to be a compressed description of the entire design philosophy of the package. What I didn't expect was how little of it lives in any one place. There's no parallelism module. The `Filter` operator has no idea it's been cloned, the channel does the load balancing for free, and the only thing that knows about any of it is a container operator whose whole job is to make copies. The shape I described at the top isn't enforced anywhere — it just falls out of which operators can see one document at a time and which ones can't.

If you want the version written by people who actually built it, the [repo README](https://github.com/couchbase/query/blob/master/README.md) walks through each statement type and marks exactly where the pipeline parallelizes and where it has to serialize. I found it much easier to read *after* working out the two-axis thing for myself, which is probably an argument for reading source before documentation.

Also: I now understand why `go someFunc()` doesn't wait for anything, and why forgetting to wait for your workers means `main` cheerfully exits and murders them mid-print. But that's a story about a `done` channel and an afternoon of confusing output, and it deserves its own post.
