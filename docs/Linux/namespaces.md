# Linux Namespaces

### Create a new namespace
A new namespace can be created using `unshare()` or `clone()`

Run a command in a new namespace.

- Usually `--fork` and `--pid` goes together to create new process in a new PID
  namespace.
- `--mount-proc` is used together with `--fork` and `--pid` to mount a new procfs
  (at /proc) containing only the PIDs in the new PID namespace.

Creating a  new `--pid` namespace requires the `CAP_SYS_ADMIN` capability.

```
$ sudo unshare --fork --ipc --pid --net --mount --mount-proc bash
```

### Enter a namespace
`setns(2)` syscall.
Need to the specify the target process with `-t`:
```
$ nsenter --net -t TARGET-PID ip a show
```

### Persistency
Namespace once created exist as long as something is using it.

Namespaces CAN'T be empty. Something must be inside it, and if not,
kernel automatically garbage collects it by reference counting.

How to occupy a namespace:
- A running process
- A bind mound `=>` kernel will maintain the NS independently of a running process.

Do it with:
```
$ mount --bind /proc/PID/ns/{uts,net,pid,...}  [ANY-PATH]
```
`mnt` NS is an exception, the mount bind can only be done in a different mount namespace:
https://stackoverflow.com/questions/34783391/why-i-couldnt-use-mount-bind-proc-pid-ns-mnt-to-another-file-in-ubuntu

### About the Namespace ID in "/proc/PID/ns/NS-NAME"

```
$ sudo readlink /proc/self/ns/mnt
mnt:[4026531840]
```

The ID is the  "inum" (inode number) field in `struct ns_common`.
See the kernel function `ns_get_name()`.
The initial `inum` values are defined in `include/linux/proc_ns.h`:
```
enum {
	PROC_ROOT_INO		= 1,
	PROC_IPC_INIT_INO	= 0xEFFFFFFFU,
	PROC_UTS_INIT_INO	= 0xEFFFFFFEU,
	PROC_USER_INIT_INO	= 0xEFFFFFFDU,
	PROC_PID_INIT_INO	= 0xEFFFFFFCU,
	PROC_CGROUP_INIT_INO	= 0xEFFFFFFBU,
	PROC_TIME_INIT_INO	= 0xEFFFFFFAU,
};
```

- For the PID NS, the allocation is dynamic, done in `create_pid_namespace(...)`, that
  calls `ns_alloc_inum(ns) -> proc_aclloc_inum()`. That means that an ID can be reused.

- For the mount NS, the initial definition is in `fs/proc/generic.c`: `PROC_DYNAMIC_FIRST`,
  and the allocation is dynamic. That means that an ID can be reused.

### Mount Namespaces
Provides an isolation of the list of mount points seen by the processes in each
NS instance. Processes in each mount NS will see distinct single-directory
hierarchies of files.

Mount namespaces have the desired property that running processes can only be moved
into the namespace down the nested hierarchy.

When a process creates a new mount namespace using clone(2) or unshare(2) with
the `CLONE_NEWNS` flag, the mount point list for the new namespace **is a copy** of
the caller's mount point list.  Subsequent modifications to the mount point list
(mount(2) and umount(2)) in either mount  namespace  will  not  (by default)
affect the mount point list seen in the other namespace.

### PID Namespaces
PID namespaces can be nested: each PID namespace has a parent, except
for the initial ("root") PID namespace.  The parent of a PID
namespace is the PID namespace of the process that created the
namespace using clone(2) or unshare(2).  PID namespaces thus form a
tree, with all namespaces ultimately tracing their ancestry to the
root namespace.  Since Linux 3.7, the kernel limits the maximum
nesting depth for PID namespaces to 32.

/proc/sys/kernel/ns_last_pid (since Linux 3.3)
This file displays the last PID that was allocated in this PID
namespace.  When the next PID is allocated, the kernel will

### User Namespaces
User namespaces can be nested; that is, each user namespace—except
the initial ("root") namespace—has a parent user namespace, and can
have zero or more child user namespaces.  The parent user namespace
is the user namespace of the process that creates the user namespace
via a call to unshare(2) or clone(2) with the CLONE_NEWUSER flag.

### Network Namespaces
Network namespaces cannot be nested. That's because, after all, an network device
can be in one and one only network namespace, so there's no point in nesting them.

How to occupy a network NS:
- with a process.
- (pseudo-filesystem nsfs-type) with a mount bind (usually in `/var/run/netns/NSNAME`)
  * the name of the file is the name of the network namespace
  * the file is a bind mount from `/proc/<PID_IN_NET_NAMESPACE>/ns/net` to `/var/run/netns/NSNAME`
  * the inode (as shown by `stat`) of `/var/run/netns/NSNAME` is the network namespace identifier.
  * the namespace exists even if there is no process associated to it, i.e. even if
  there is no process for which the inode ID of the symlink `/proc/PID/ns/net` is
  the inode ID of `/var/run/netns/NSNAME`.

Once both no process is in the namespace, and no nsfs mountpoint exits for the
namespace, the namespace disappears.

You can very well create a network namespace for init:
```
$ sudo touch /var/run/netns/init_netns
$ sudo mount -o bind /proc/1/ns/net /var/run/netns/init_netns
$ sudo ip netns ls
init_netns
$ sudo ip netns exec init_netns ip a
....# same stuff you would see with `ip a` in the init namespace...
```
#### Concepts
Network namespace NAME:
- created with `ip netns add NETNSNAME`.

Network namespace ID:
> NOTE: nsid is used when communicating with the kernel using rt netlink.
- created with `ip netns add NETNSNAME NSID`
- created with `ip netns set NETNSNAME NSID`
- assigned automatically with `ip link set IFNAME netns NETNSNAME`

Network namespace INODE (identifier):
  * shows up with `lsns -t net`
  * shows up as `ls -ls /proc/PID/ns/net`
  * it means that there is a process associated to the namespace.

#### ip netns add
`ip netns add foobar` will add a new mount point under `/run/netns/foobar` of type
`nsfs`. That is to keep a reference to a namespace when there is no process that
joined it. Proof:
```
$ sudo strace -e trace=mount,openat,unshare ip netns add foobar
...
openat(AT_FDCWD, "/proc/self/ns/net", O_RDONLY) = 4
mount("", "/var/run/netns", 0x55a3f42f99a5, MS_REC|MS_SHARED, NULL) = 0     ### <--- This is actually a tmpfs mountpoint
openat(AT_FDCWD, "/var/run/netns/foobar", O_RDONLY|O_CREAT|O_EXCL, 000) = 5
unshare(CLONE_NEWNET)                   = 0
mount("/proc/self/ns/net", "/var/run/netns/foobar", 0x55a3f42f99a5, MS_BIND, NULL) = 0
```

#### sysfs / iproute2
iproute2 (netlink) manages network devices in the namespace it is run.

But, if you start a process in a new network namespace using e.g. `unshare --net ...`,
that process can still see all network devices in the initial namespaces via
sysfs `/sys/class/net`.

To solve this, `ip netns exec FOO ...` (but not `ip netns add FOO`) also unshares
the mount namespace and remounts /sys/ inside it (by doing `mount --make-shared /var/run/netns`).

#### Different ways to setup a network namespace
- Docker:
  * Network namespace ID: YES
  * Network namespace NAME: NO
    - The mount point for the net ns name is instead in `/run/docker/netns/`
      Hack to have Docker namespaces show up in `ip netns ls`:
      ```
      sudo touch /run/netns/docker-1
      sudo mount -o bind /proc/<CONTAINER_PID>/ns/net /run/netns/docker-1
      sudo ip netns exec docker-1 ...
      ```
  * Network namespace INODE: YES (the container process)

- Podman (root):
  * Network namespace ID: YES
  * Network namespace NAME: YES (cni-...)
  * Network namespace INODE: YES (the container process)

- `unshare`:
  * Network namespace ID: NO
  * Network namespace NAME: NO
  * Network namespace INODE: YES (the unshared process)

- `ip netns add NETNSNAME`:
  * Network namespace ID: NO
    - no NSID assigned by default.
    - NSID can be set with `ip netns set NETNSNAME NSID` or at creation with
      `ip netns add NETNSNAME NSID`.
    - a NSID is set automatically when moving an interface to a named NSID:
     `ip link set IFNAME netns NETNSNAME`
  * Network namespace NAME: YES (cni-...)
  * Network namespace INODE: NO

#### References
https://serverfault.com/questions/961504/cannot-create-nested-network-namespace
https://unix.stackexchange.com/questions/471122/namespace-management-with-ip-netns-iproute2/471214#471214
