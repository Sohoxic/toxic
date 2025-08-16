---
title: "Go vs JavaScript: Understanding the Concurrency Execution Models"
template: light-theme.html
---




## Paragraph 1: JavaScript's async/await

> Most JavaScript developers switching to Go often ask "where's async/await?" and it reveals a fundamental misunderstanding of execution models. In JavaScript, async/await exists because V8 runs on a single OS thread with an event loop. Every syscall would block the entire process, so we needed continuation-passing style wrapped in promises. Async/await is syntactic sugar over state machines that compile function bodies into multiple resumption points, yielding execution back to the event loop scheduler.

### Explanation

- **"Where's async/await?"**  
  JavaScript developers expect a language feature for handling asynchronous operations, but Go handles it differently.

- **"V8 runs on a single OS thread with an event loop."**  
  JavaScript (e.g., in browsers or Node.js) is single-threaded with an event loop to handle asynchronous operations.

- **"Every syscall would block the entire process..."**  
  Blocking system calls would halt execution, so async was required.

- **"Continuation-passing style wrapped in promises."**  
  JavaScript used callbacks, then Promises to model async behavior.

- **"Async/await is syntactic sugar over state machines..."**  
  `async/await` makes async code look synchronous by compiling it into resumable state machines.

---

## Paragraph 2: Go's M:N threading and netpoller

> Go doesn't need async/await because it implements M:N threading. The runtime multiplexes M goroutines across N OS threads using a work-stealing scheduler. When a goroutine makes a blocking syscall, the runtime detects this via netpoller (epoll/kqueue) integration and parks the goroutine, moving the OS thread to service other runnable goroutines from the global or local run queues. The segmented stacks start at 2KB and grow dynamically, allowing millions of goroutines with minimal memory overhead.

### Explanation

- **"M:N threading."**  
  Go schedules many goroutines onto fewer OS threads.

- **"Work-stealing scheduler."**  
  Go's scheduler dynamically balances goroutines across threads.

- **"Blocking syscall and netpoller."**  
  Blocking operations are intercepted by Go's runtime, allowing the OS thread to do other work.

- **"Segmented stacks."**  
  Goroutines use minimal memory, enabling millions of them to run.

---

## Paragraph 3: Technical differences in execution models

> The technical difference is fundamental. JavaScript's async transforms your control flow into a continuation monad that gets scheduled cooperatively. You're explicitly managing asynchrony at the language level. Go's runtime handles preemptive scheduling transparently. A blocking read() syscall gets intercepted by the runtime, the goroutine gets parked in the netpoller's waiting list, and execution continues elsewhere. When the file descriptor becomes ready, the runtime resumes the goroutine.

### Explanation

- **"Continuation monad, cooperatively scheduled."**  
  JavaScript async functions pause and resume with developer-managed control.

- **"Explicit async control."**  
  Developers must use `async` and `await`.

- **"Go's preemptive scheduling."**  
  Go's runtime handles all concurrency transparently.

- **"Blocking syscalls are handled internally."**  
  Goroutines are paused and resumed automatically without developer intervention.

---

## Paragraph 4: Go code looks synchronous but is concurrent

> This is why Go code looks "boring" to JavaScript developers. There's no colored function problem, no promise microtask queue semantics, no await keyword infecting your call stack. You write synchronous-looking code that gets automatically transformed into efficient asynchronous operations by the compiler and runtime. The goroutine scheduler achieves better cache locality and lower context switch overhead than JavaScript's event loop because it's operating at the language runtime level, not forcing userland state machines.

### Explanation

- **"Go code looks boring."**  
  Because it avoids special async syntax and appears synchronous.

- **"No colored function problem."**  
  Functions aren't classified as async vs sync — all functions are composable.

- **"No microtask semantics."**  
  No promise queues or await interleaving.

- **"Compiler and runtime transform code."**  
  Goroutines make code efficient under the hood, while the syntax remains clean.

- **"Better performance characteristics."**  
  Go achieves better cache usage and avoids OS-level context switches.

---

## Paragraph 5: Eliminating async contagion in Go

> Go's approach eliminates the async contagion problem entirely. In JavaScript, once you call an async function, everything up the call stack must become async. Go's transparent I/O multiplexing means you can compose blocking and non-blocking operations without syntactic interleaving. The runtime's integrated netpoller and work-stealing scheduler provide better performance characteristics than userland promise queues and microtask scheduling.

### Explanation

- **"Async contagion."**  
  In JavaScript, `async` propagates up the stack, affecting the entire codebase.

- **"Go allows mixing of operations."**  
  Go code can block or not block without changing the function signature or syntax.

- **"Transparent I/O multiplexing."**  
  Handled entirely by Go’s runtime, not the developer.

- **"Better performance characteristics."**  
  Go’s netpoller and scheduler are more efficient than JavaScript’s userland mechanisms.

---

## Summary Table

| Feature | JavaScript | Go |
|--------|-------------|----|
| Concurrency Model | Single-threaded, event loop + Promises | M:N threading with goroutines |
| Async Syntax | Explicit (`async/await`) | Implicit (no syntax) |
| Scheduler | Cooperative (microtask/event loop) | Preemptive (runtime scheduler) |
| Async Contagion | Yes (`async` infects call stack) | No |
| Stack Size | Large (1MB+) per thread | Small (2KB, grows dynamically) |
| Performance | Depends on event loop, microtasks | Efficient due to netpoller + scheduler |
