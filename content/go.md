---
title: Understanding Type Inference in Go
template: dark-theme.html
---

In Go, **numbers like `1`, `2.5`, `-3` don't have a type until you use them** in a context where a type is expected.

Go allows the compiler to **infer the type** of a number based on how it's being used.

---

## 📌 Statement

> A number can be given a type by using it in a context that requires one, such as a variable assignment or function call.  
> For example, here `math.Sin` expects a `float64`.

---

##  Example

```go
import "math"

x := math.Sin(1)
```

### What's happening here:
- 1 is a numeric literal without an explicit type.

- math.Sin is a function that expects a float64 parameter.

> Since you're passing 1 into math.Sin, Go automatically treats 1 as float64. Even though you didn’t write 1.0 or cast it like float64(1), Go infers the type because of the context.

