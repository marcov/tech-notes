# (Some) Compiler Optimization Side effects

## Store Tearing

Store tearing occurs when the compiler uses multiple store instructions for a
single access.

For example, one thread might store 0x12345678 to a four-byte integer variable
at the same time as another thread stored 0xabcdef00.
If the compiler used 16-bit stores for either access, the result might well be
0x1234ef00, which could come as quite a surprise to code loading from this
integer.
There are CPUs that feature small immediate values, and on such CPUs, the
compiler can be tempted to split a 64-bit store into two 32-bit stores in order
to reduce the overhead of explicitly forming the 64-bit constant in a register,
even on a 64-bit CPU.

Note that this tearing can happen even on properly aligned and
machine-word-sized accesses, and even for volatile stores.

## Load Fusing

https://lwn.net/Articles/793253/

Load fusing occurs when the compiler uses the result of a prior load from a
given variable instead of repeating the load. Not only is this sort of
optimization just fine in single-threaded code, it is often just fine in
multithreaded code. Unfortunately, the word "often" hides some truly annoying
exceptions, including the one called out in the ACCESS_ONCE() article.

We do occasionally use READ_ONCE() to prevent load-fusing optimizations that
would otherwise cause the compiler to turn while-loops into if-statements
guarding infinite loops.

Load fusing can be prevented by using READ_ONCE() or by enforcing ordering
between the two loads using barrier(), smp_rmb().

### ACCESS_ONCE()

ACCESS_ONCE: its purpose is to ensure that the value passed as a parameter is
accessed exactly once by the generated code.

E.g., this code:
```
for (;;) {
	struct task_struct *owner;

	owner = ACCESS_ONCE(lock->owner);
	if (owner)
	    break;
    ...
}
```

Cannot be optimized into this:

```
struct task_struct *owner;
owner = ACCESS_ONCE(lock->owner);
for (;;) {
	if (owner && !mutex_spin_on_owner(lock, owner))
	    break;
    ...
}
```

The compiler misses that a value may be changed by another thread of execution.

```
 #define ACCESS_ONCE(x) (*(volatile typeof(x) *)&(x))
```
In other words, it works by turning the relevant variable, temporarily, into a
volatile type.

It is only in places where shared data is accessed without locks (or explicit
barriers) that a construct like ACCESS_ONCE() is required.

### READ_ONCE()

Pretty much similar to ACCESS_ONCE():
```
#define __READ_ONCE(x)	(*(const volatile __unqual_scalar_typeof(x) *)&(x))
```

## What the compiler can / cannot do

### Can merge multiple writes to a shared variable with a single one (even with locks)

This does not violate SC.

E.g.,
```
lock_shared_ctr

for (i = 0; i < N; i++)
    shared_ctr++

unlock_shared_ctr
```

can become:
```
lock_shared_ctr

r1 = shared_ctr
for (i = 0; i < N; i++)
    r1++
shared_ctr = r1

unlock_shared_ctr
```

### Invent read

Used to implement conditional write via a register.

### Cannot
It must never invent a write to a variable that would not have been written to
seq cst execution.

# Synchronization Operation

5 The library defines a number of atomic operations (7.17) and operations on
mutexes (7.26.4) that are specially identified as synchronization operations.

These operations play a special role in making assignments in one thread
visible to another. A synchronization operation on one or more memory locations
is either an acquire operation, a release operation, both an acquire and
release operation, or a consume operation.

A synchronization operation without an associated memory location is a fence
and can be either an acquire fence, a release fence, or both an acquire and
release fence.

# Data race
Two conflicting actions in different threads, at least one of which is not atomic,
and neither happens before the other.

data race == undefined behavior.

Two threads accessing the same memory location, and at least one of the access
is a write.

# Controlling Compiler Optimizations

Methods to control and/or make compiler memory accesses deterministic in
multithreaded applications:

- Using locks (mutex, spinlocks, ...).
- Using atomics
- Using fences

## Atomics

Atomics are a way to control compiler optimization and reordering.

### Acquire and Release

- Compiler can only see memory access by a single thread.

- How to think about atomic:

```
A

vvv: OK - ^^^: blocked

atomic_read  <=> lock.acquire() (acquire exclusion)

B

atomor_write <=> lock.release() (release exclusion)

^^^: OK  - vvv: blocked

C
```

Acquire and release are one way barrier.

The compiler:
- cannot move B outside of the region.
- can move A and C inside the region.
- cannot move C before the region: it cannot move up across an acquire.
- cannot move A after the region: it cannot move down across a release.

In addition, for sequential consistent model, you cannot reorder
require/release, e.g. you cannot move an acquire (read) before a release
(store).

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

## volatile

It is an unoptmizable variable, for talking to something outside the program.
It is outside the memory model.

It does not guarantee atomicity (read / write all or nothing).

Being unoptimizable, the compiler cannot eg fold multiple writes in a single one.

### Linux kernel perspective
Sum up from: https://lwn.net/Articles/233479/

The purpose of volatile is to force an implementation to **suppress optimizations**
that could otherwise occur. For example, for a machine with memory-mapped
input/output, a pointer to a device register might be declared as a pointer to
volatile, in order to prevent the compiler from removing apparently redundant
references through the pointer.

The point that Linus often makes with regard to volatile is that its purpose is
to suppress optimization, which is almost never what one really wants to do.
In the kernel, one must protect accesses to data against race conditions, which
is very much a different task.

Given:
```
    spin_lock(&the_lock);
    do_something_on(&shared_data);
    do_something_else_with(&shared_data);
    spin_unlock(&the_lock);
```
The spinlock primitives act as memory barriers - they are explicitly written to
do so - meaning that data accesses will not be optimized across them.

If shared_data were declared volatile, the locking would still be necessary.
But the compiler would also be prevented from optimizing access to shared within
the critical section, when we know that nobody else can be working with it.
While the lock is held, shared_data is not volatile.

> "Data isn't volatile - _accesses_ are volatile".

that means:

> It's not the memory location that is volatile, it is really the
> _access_ that is volatile.

that means, you should only use volatile when accessing a location, not when
declaring a variable. The same memory location may be completely stable in other
access situations, i.e. under a lock

Spinlocks and mutexes both function as optimization barriers, meaning that they
prevent optimizations on one side of the barrier from carrying over to the
other.

When dealing with shared data, proper locking makes volatile unnecessary - and
potentially harmful. The volatile storage class was originally meant for
memory-mapped I/O registers.

### More on volatile

Volatile multi-threaded applications does **NOT**:
- provide any synchronization,
- create memory fences,
- ensure the order of execution of operations,
- make operations atomic.

It should be used as a hint to the compiler similarly to "const".

From "The C Programming Language" book:

>Do not use volatile except in low-level code that deals directly with
>hardware.
>
>Do not assume volatile has special meaning in the memory model. It does not.
>It is not -- as in some later languages -- a synchronization mechanism. To get
>synchronization, use atomic, a mutex, or a condition_variable.

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

### Tests with atomic

Atomic alone is not magic, it is not enough to force the compiler do something.

E.g.
```
std::atomic<int> foo;
foo = 1;

foo = 2;
foo = 3;
while (foo) {
    sleep(1);
}
```

Gets optimized the hell out of it, exactly as if using plain int for foo:
```
   0x100003f80 <main()+16>:     mov    $0x1,%edi
   0x100003f85 <main()+21>:     call   0x100003f8c
   0x100003f8a <main()+26>:     jmp    0x100003f80 <main()+16>
```

This was observed with `clang-12 -03`.

---

By using `volatile`:
```
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
folder into a single store of imm. 3).

---

If we insert a library call to an opaque function before the loop (even if we
know the call takes the argument as read only, and _APPARENTLY_ event if the
function argument is `const int*`) then things starts to change:

```
int foo;
foo = 1;

foo = 2;
printf("foo: %p\n", &foo);

...
```

- if the loop is a `sleep(1)`, sleep can be considered as another opaque function,
so it behaves again as a barrier and there is no folding:
```
...

while (foo) {
    sleep(1);
}
```

- if the loop is just incrementing a local counter

  * plain `int` makes the compiler fold and optimize out loads.
    ```
    ...

    int ctr = 0;
    while (foo) {
        ctr++;
    }
    printf("ctr is %d\n", ctr);
    ```

  * declaring `foo` as `std::atomic` acts as a barrier and forces loads.
    ```
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

```
static std::atomic<int> foo;

int main() {
    foo = -1

    int ctr = 0;
    while (foo) {
        ctr++
    }
```
