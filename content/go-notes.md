
> *All of these notes examples have either been taken from [Go Dev Tour](https://go.dev/tour/) or from my thoughts/learnings elsewhere.*
# Packages
Every Go program is made up of packages.

Programs start running in package `main`.

This program is using the packages with import paths `"fmt"` and `"math/rand"`.

By convention, the package name is the same as the last element of the import path. For instance, the `"math/rand"` package comprises files that begin with the statement package rand.

### Custom Go Package usage:

```
go-example/
├── main.go
└── mymath/
    └── math.go
```

```go
package mymath

// Add adds two integers.
func Add(a int, b int) int {
    return a + b
}

// Multiply multiplies two integers.
func Multiply(a int, b int) int {
    return a * b
}
```

Using the package mymath in main.go

```go
package main

import (
    "fmt"
    "go-example/mymath" // Use the module path + package folder
)

func main() {
    sum := mymath.Add(3, 4)
    product := mymath.Multiply(3, 4)

    fmt.Println("Sum:", sum)
    fmt.Println("Product:", product)
}

```

# Imports
Factored Imports:

```go
import (
    "math"
    "fmt"
)
```
Normal Import:
```go
import "fmt"
import "math"
```

# Exported names
In Go, a name is `exported` if it begins with a *capital letter*. For example, Pizza is an exported name, as is Pi, which is exported from the math package.

When importing a package, you can *refer only to its exported names*. Any `"unexported"` names are not accessible from outside the package.

# Functions
When two or more consecutive named function parameters share a type, you can omit the type from all but the last.

In this example, we shortened
```go
x int, y int
```
to
```go
x, y int
```

A function can return any number of results.
```go
package main

import "fmt"

func swap(x, y string) (string, string) {
	return y, x
}

func main() {
	a, b := swap("hello", "world")
	fmt.Println(a, b)
}
```
