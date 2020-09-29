# Rootless Containers

## pivot_root
From pivot_root(2):
    pivot_root() changes the root directory and the current working
    directory of each process or thread in the same mount namespace to
    new_root if they point to the old root directory.  (See also NOTES.)
    On the other hand, pivot_root() does not change the caller's current
    working directory (unless it is on the old root directory), and thus
    it should be followed by a chdir("/") call.

As found in "Rootless Containers with runC" -- Aleksa Sarai
```
$ unshare -UrmunipCf bash

# These 2 are needed for pivot_root to work:
$ mount --make-rprivate /
$ mount --rbind rootfs/ rootfs/

# (not needed for pivot_root POC)
$ mount -t proc proc rootfs/proc
$ mount -t tmpfs tmpfs rootfs/dev
$ mount -t devpts -o newinstance devpts rootfs/dev/pts
$ # ... skipping over a lot more mounting ...

$ pivot_root rootfs/ rootfs/.pivot_root && cd /
$ mount --make-rprivate /.pivot_root && umount -l /.pivot_root

$ exec bash # finally
```
