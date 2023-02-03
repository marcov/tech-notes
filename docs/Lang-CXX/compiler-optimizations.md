## Compiler Optimizations - side effects

## Controlling Compiler Optimizations

Methods to control and/or make compiler memory accesses deterministic in
multithreaded applications:

- Using locks (mutex, spinlocks, ...).
- Using atomics
- Using fences

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

## ACCESS_ONCE()

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

## READ_ONCE()

Pretty much similar to ACCESS_ONCE():
```
#define __READ_ONCE(x)	(*(const volatile __unqual_scalar_typeof(x) *)&(x))
```

## What the compiler can / cannot do

## Can merge multiple writes to a shared variable with a single one (even with locks)

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

## Invent read

Used to implement conditional write via a register.

## Cannot

It must never invent a write to a variable that would not have been written to
seq cst execution.
