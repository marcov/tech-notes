# Containers Notes

## PID 1 and signals
When a container process is running with PID 1, i.e. with no init process  (i.e.,
with no `--init` option), then by default all signals sent to the process are masked.
So, to receive signals, the process needs to explicitly enable handling of
those signals.
That's because in Linux by default PID 1 has signals masked.

## Container Rootfs
### Using `procfs`
- Retrieve the container rootfs path from host POV: `/proc/<container-pid>/mounts`

- Access to the rootfs filesystem, without knowing the mount point (requires sharing
  the PID namespace):

   * `/proc/<PID>/root`
   * `/proc/<PID>/cwd` + `[relative path...]`, e.g. `/proc/<PID>/cwd/../../../../../../`

From `proc(5)`:
    /proc/[pid]/root
      UNIX and Linux support the idea of a per-process root of the
      filesystem, set by the chroot(2) system call.  This file is a
      symbolic link that points to the process's root directory, and
      behaves in the same way as exe, and fd/*.

      Note however that this file is not merely a symbolic link.  It
      provides the same view of the filesystem (including namespaces
      and the set of per-process mounts) as the process itself.  An
      example illustrates this point.  In one terminal, we start a
      shell in new user and mount namespaces, and in that shell we
      create some new mount points:

      -- CUT --

      In a multithreaded process, the contents of the
      /proc/[pid]/root symbolic link are not available if the main
      thread has already terminated (typically by calling
      pthread_exit(3)).

      Permission to dereference or read (readlink(2)) this symbolic
      link is governed by a ptrace access mode
      PTRACE_MODE_READ_FSCREDS check; see ptrace(2).


    /proc/[pid]/cwd
      This  is  a  symbolic  link to the current working directory of the process.
      To find out the current working directory of process 20, for instance,
      you can do this:

          $ cd /proc/20/cwd; /bin/pwd

      Note that the pwd command is often a shell built-in, and might not work properly.
      In bash(1), you may use pwd -P.

      In a multithreaded process, the contents of this symbolic link are not
      available if the main thread has already terminated (typically by calling
      pthread_exit(3)).

      Permission   to   dereference   or   read   (readlink(2))  this  symbolic
      link  is  governed  by  a  ptrace  access  mode PTRACE_MODE_READ_FSCREDS
      check; see ptrace(2).

### Using runC
```
$ runc state <container-id>
```
When runC is the Docker runtime, you need to also pass the option: `--root /var/run/docker/runtime-runc/moby`

