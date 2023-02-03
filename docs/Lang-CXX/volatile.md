# volatile

It is an un-optimizable variable, for talking to something outside the program.
It is outside the memory model.

It does not guarantee atomicity (read / write all or nothing).

Being un-optimizable, the compiler cannot eg fold multiple writes in a single
one.

## Linux kernel perspective on volatile

Sum up from: https://lwn.net/Articles/233479/

The purpose of volatile is to force an implementation to **suppress
optimizations** that could otherwise occur. For example, for a machine with
memory-mapped input/output, a pointer to a device register might be declared as
a pointer to volatile, in order to prevent the compiler from removing
apparently redundant references through the pointer.

The point that Linus often makes with regard to volatile is that its purpose is
to suppress optimization, which is almost never what one really wants to do. In
the kernel, one must protect accesses to data against race conditions, which is
very much a different task.

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

## More on volatile

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

