---
title: Go Code Review Best Practices
description: Go code review focusing on error handling, concurrency, and idiomatic Go patterns.
allowed-tools:
  - Bash(go test:*)
  - Bash(go mod:*)
---

# Go Code Review Best Practices

## Check for Existing Patterns First

Before implementing new functionality, search the codebase for existing utilities:

```
ReferenceSearch(query="HTTP client with retry")
ReferenceSearch(query="structured logging")
ReferenceSearch(query="config loading")
ReferenceSearch(query="database connection pool")
```

Common things to check before rolling your own:

| Need              | Search Query                        |
|-------------------|-------------------------------------|
| HTTP clients      | `"http client"`                     |
| Logging           | `"structured logging" OR "slog"`    |
| Configuration     | `"config" OR "viper"`               |
| Authentication    | `"auth" OR "jwt" OR "oauth"`        |
| Database          | `"database" OR "postgres" OR "sql"` |

## Critical Issues (Must Fix)

### Error Handling

```go
// ❌ BAD: Ignoring errors
result, _ := doSomething()

// ❌ BAD: Swallowing error context
if err != nil {
    return errors.New("operation failed")
}

// ✅ GOOD: Wrap with context
if err != nil {
    return fmt.Errorf("failed to fetch user %s: %w", userID, err)
}
```

### Nil Pointer Dereference

```go
// ❌ BAD: No nil check
func process(user *User) string {
    return user.Name  // panics if user is nil
}

// ✅ GOOD: Check for nil
func process(user *User) string {
    if user == nil {
        return ""
    }
    return user.Name
}
```

### Resource Leaks

```go
// ❌ BAD: Response body not closed
resp, err := http.Get(url)
if err != nil {
    return err
}
// Process response... but body never closed!

// ✅ GOOD: Always close response body
resp, err := http.Get(url)
if err != nil {
    return err
}
defer resp.Body.Close()
```

### Context Propagation

```go
// ❌ BAD: No context threading
func fetchUser(id string) (*User, error) {
    return db.Query("SELECT * FROM users WHERE id = ?", id)
}

// ✅ GOOD: Pass context through call chain
func fetchUser(ctx context.Context, id string) (*User, error) {
    return db.QueryContext(ctx, "SELECT * FROM users WHERE id = ?", id)
}
```

## Concurrency

### Goroutine Leaks

```go
// ❌ BAD: Goroutine with no exit condition
go func() {
    for {
        process() // runs forever, no way to stop
    }
}()

// ✅ GOOD: Use context for cancellation
go func() {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            process()
        }
    }
}()
```

### Race Conditions

```go
// ❌ BAD: Shared state without synchronization
var counter int
go func() { counter++ }()
go func() { counter++ }()

// ✅ GOOD: Use sync primitives
var mu sync.Mutex
var counter int
go func() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}()

// ✅ ALSO GOOD: atomic for simple counters
var counter atomic.Int64
go func() { counter.Add(1) }()
```

### Channel Patterns

```go
// ❌ BAD: Sending to closed channel (panics)
close(ch)
ch <- value // panic!

// ✅ GOOD: Use select with done channel
select {
case ch <- value:
case <-done:
    return
}
```

### Defer in Loops

```go
// ❌ BAD: Defers accumulate until function returns
for _, file := range files {
    f, _ := os.Open(file)
    defer f.Close() // all defers run at end of function, not loop iteration!
}

// ✅ GOOD: Wrap in a function
for _, file := range files {
    func() {
        f, _ := os.Open(file)
        defer f.Close() // runs at end of anonymous func
        process(f)
    }()
}
```

## Idiomatic Go

### Interface Design

```go
// ❌ BAD: Large interface (hard to implement/mock)
type UserService interface {
    Create(user User) error
    Update(user User) error
    Delete(id string) error
    Get(id string) (User, error)
    List() ([]User, error)
    Search(query string) ([]User, error)
}

// ✅ GOOD: Small, focused interfaces
type UserReader interface {
    Get(id string) (User, error)
    List() ([]User, error)
}

type UserWriter interface {
    Create(user User) error
    Update(user User) error
    Delete(id string) error
}
```

### Error Types

```go
// ❌ BAD: Comparing error strings
if err.Error() == "not found" {

// ✅ GOOD: Sentinel errors
var ErrNotFound = errors.New("not found")
if errors.Is(err, ErrNotFound) {

// ✅ GOOD: Custom error types
type NotFoundError struct {
    ID string
}
func (e *NotFoundError) Error() string {
    return fmt.Sprintf("resource %s not found", e.ID)
}
var nfe *NotFoundError
if errors.As(err, &nfe) {
```

### Struct Initialization

```go
// ❌ BAD: Positional initialization (fragile)
user := User{"John", 30, "john@example.com"}

// ✅ GOOD: Named fields
user := User{
    Name:  "John",
    Age:   30,
    Email: "john@example.com",
}
```

## Performance

### String Building

```go
// ❌ BAD: String concatenation in loop
var result string
for _, s := range items {
    result += s // O(n²) allocations!
}

// ✅ GOOD: Use strings.Builder
var builder strings.Builder
for _, s := range items {
    builder.WriteString(s)
}
result := builder.String()
```

### Preallocate Slices

```go
// ❌ BAD: Growing slice repeatedly
var results []Item
for _, id := range ids {
    results = append(results, fetchItem(id))
}

// ✅ GOOD: Preallocate when size known
results := make([]Item, 0, len(ids))
for _, id := range ids {
    results = append(results, fetchItem(id))
}
```

### Map Preallocation

```go
// ❌ BAD: Map grows dynamically
m := make(map[string]int)

// ✅ GOOD: Preallocate when size known
m := make(map[string]int, expectedSize)
```

## Testing

### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Test Helpers

```go
// Use t.Helper() for test utilities
func assertEqual(t *testing.T, got, want interface{}) {
    t.Helper() // Marks this as helper - errors report caller's line
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

## Static Analysis

Run `/lint` to handle all linting (tool setup, `go vet`, `golangci-lint`). It auto-installs missing tools.

For review-specific checks beyond linting (mod health, tests, TODOs), use the review script:

```bash
# Full Go review (mod checks + tests — run after /lint)
bash {baseDir}/scripts/analyze-go.sh

# With auto-fix
bash {baseDir}/scripts/analyze-go.sh --fix

# Skip tests
SKIP_TESTS=true bash {baseDir}/scripts/analyze-go.sh
```

## Go 1.21+ Features

### `slices` and `maps` packages

```go
// Use standard library generics
import "slices"

slices.Sort(items)
slices.Contains(items, target)
idx := slices.Index(items, target)
```

### Structured Logging (slog)

```go
import "log/slog"

slog.Info("user created",
    "user_id", user.ID,
    "email", user.Email)
```

### Error Wrapping

```go
// ❌ BAD: Loses error context
if err != nil {
    return errors.New("operation failed")
}

// ✅ GOOD: Wrap with context
if err != nil {
    return fmt.Errorf("failed to fetch user %s: %w", userID, err)
}
```

### Struct Initialization

```go
// ❌ BAD: Positional initialization (fragile)
user := User{"John", 30, "john@example.com"}

// ✅ GOOD: Named fields
user := User{
    Name:  "John",
    Age:   30,
    Email: "john@example.com",
}
```

## Security Checklist

- [ ] SQL queries use parameterized statements
- [ ] User input is validated and sanitized
- [ ] Secrets not hardcoded (use environment variables)
- [ ] TLS/HTTPS used for external connections
- [ ] Rate limiting on public endpoints
- [ ] No sensitive data in logs
- [ ] Proper authentication/authorization checks
