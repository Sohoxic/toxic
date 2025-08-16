---
title: Go `if` Statement with Short Variable Declaration
template: light-theme.html
---

This Go code demonstrates how to use a short variable declaration (`:=`) inside an `if` statement and how control flows through multiple conditional branches.


## ✅ Code

```go
if num := 9; num < 0 {
    fmt.Println(num, "is negative")
} else if num < 10 {
    fmt.Println(num, "has 1 digit")
} else {
    fmt.Println(num, "has multiple digits")
}
```

> Here num is getting declared at the start of the if statement here `num := 9` and then directly being used to check the conditions