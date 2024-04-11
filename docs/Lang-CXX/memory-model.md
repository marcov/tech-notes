# C / C++ Memory Model (Atomics et al.)

## Data race

Two conflicting actions in different threads, at least one of which is not
atomic, and neither happens before the other.

data race == undefined behavior.

Two threads accessing the same memory location, and at least one of the access
is a write.

## Register Allocation

Q: Is is always true that a local auto variable gets allocated in memory?

```cpp
void foo()
{
    int bar;

    std::cout << "bar is " << &bar;
}
```

A: If the address of a variable is taken, the variable better be stored in a
location that has an address. A register doesn’t have an address, so it has to
be stored in memory whether it’s available or not.

## Synchronization Operation

The library defines a number of atomic operations (7.17) and operations on
mutexes (7.26.4) that are specially identified as synchronization operations.

These operations play a special role in making assignments in one thread
visible to another. A synchronization operation on one or more memory locations
is either an acquire operation, a release operation, both an acquire and
release operation, or a consume operation.

A synchronization operation without an associated memory location is a fence
and can be either an acquire fence, a release fence, or both an acquire and
release fence.

## Atomics

Atomics are a way to control compiler optimization and reordering.

### Acquire and Release

- Compiler can only see memory access by a single thread.

- How to think about atomic: acquire and release are one way barrier.

```c
A;              // A can move after atomic_read();

// move down: OK
atomic_read();  // <=> lock.acquire() (acquire exclusion)
// move up:   BLOCKED

B;             // B cannot move before atomic_read() or after atomic_write()

// move down: BLOCKED
atomic_write() <=> lock.release() (release exclusion)
// move up:   OK

C;              // C can move before atomic_write();
```

The compiler:

- cannot move B outside of the region.
- can move A and C inside the region.
- cannot move C before the region: it cannot move up across an acquire.
- cannot move A after the region: it cannot move down across a release.

In addition, for sequential consistent model, you cannot reorder
acquire with release, e.g., this:

```c
atomic_write();
atomic_read();
```

cannot be reordered into:

```c
atomic_read();
atomic_write();
```

---

MV: So apparently an atomic read prevents load fusing:

E.g. given:

```
read variable
if set
  foo

read variable
if set
    bar
bar
```

it can be load fused with:

```
register = variable

if register set
    foo
    bar
```

With atomic read:

```
// nothing can move up
vvv  atomic_read vvv
if set
  foo

// nothing can move up
vvv  atomic_read vvv
if set
    bar
```

At most, bar can be executed before foo.

### std::atomic

Default seq const.
Each individual write of an atomic:
- guaranteed to be all or nothing
- guaranteed to be executed in order

### LLVM on atomics

Folding a load: Any atomic load from a constant global can be constant-folded,
because it cannot be observed. Similar reasoning allows SROA (scalar
replacement of aggregates) with atomic loads and stores.

## Fences

Explicit barriers against reordering.

CONS:

- Non portables thru OS and architectures.
- You need to write the right one each time you used a shared variable
- Worsen performances: they stop everything, does not only affect one shared
  var, but everything.

## Misc 2

Compiler can optimize only when it has visibility, e.g. it has visibility of
what happens inside a function.

Compiler has to assume that any opaque function call is a full barrier, so
it cannot move things around.

Opaque function: a fn the compiler has no prior information about.
This implies that the compiler can make no assumptions about the side effects
of the function call.

### Tests with atomic

Atomic alone is not magic, it is not enough to force the compiler do something.

E.g.

```c
std::atomic<int> foo;
foo = 1;

foo = 2;
foo = 3;
while (foo) {
    sleep(1);
}
```

Gets optimized the hell out of it, exactly as if using plain int for foo:

```c
   0x100003f80 <main()+16>:     mov    $0x1,%edi
   0x100003f85 <main()+21>:     call   0x100003f8c
   0x100003f8a <main()+26>:     jmp    0x100003f80 <main()+16>
```

This was observed with `clang-12 -03`.

---

By using `volatile`:

```c
static inline void loop(volatile int& bar)
{
    while (foo) {
        sleep(1);
    }
}

int foo;
foo = 1;

foo = 2;
foo = 3;

loop(foo);
```

you force the compiler to always do a memory access (the three stores gets
folded into a single store of imm. 3).

---

If we insert a library call to an opaque function before the loop (even if we
know the call takes the argument as read only, and _APPARENTLY_ event if the
function argument is `const int*`) then things starts to change:

```c
int foo;
foo = 1;

foo = 2;
printf("foo: %p\n", &foo);

//...
```

- if the loop is a `sleep(1)`, sleep can be considered as another opaque function,
so it behaves again as a barrier and there is no folding:

```c
//...

while (foo) {
    sleep(1);
}
```

- if the loop is just incrementing a local counter

  * plain `int` makes the compiler fold and optimize out loads.

    ```c
    //...

    int ctr = 0;
    while (foo) {
        ctr++;
    }
    printf("ctr is %d\n", ctr);
    ```

  * declaring `foo` as `std::atomic` acts as a barrier and forces loads.

    ```c
    ...

    int ctr = 0;
    while (foo) {
        ctr++;
    }
    printf("ctr is %d\n", ctr);
    ```
---

Atomics starts to have sense when e.g. moving the variable as static, instead of
local. Now, using atomic instead of plain int prevent the compiler to optimize
loads.

```c
static std::atomic<int> foo;

int main() {
    foo = -1

    int ctr = 0;
    while (foo) {
        ctr++
    }
```

## std::atomic_ref and pointers to atomic plain data

C++ introduced atomic_ref to allow atomic access to any kind of data, even when
not declared atomic
