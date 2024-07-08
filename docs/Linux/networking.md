# Linux Networking

## Kernel data structures

- `struct socket`, interface to the userspace, created by `sys_socket()`.
- `struct sock`, interface to the network layer (L3).

`socket.ops`: callbacks for the socket. Interface to userspace.

## Ephemeral Ports

This is the range of ports that is not part of the well-known ports.
When a process calls connect(2) without binding to a specific port, it is assigned
a source port from the ephemeral port range. On Linux the range is specified in
`/proc/sys/net/ipv4/ip_local_port_range`.

## Raw sockets

Normal `socket(domain, type, protocol)` calls do not need the third `protocol`
parameter, The  protocol is implied from the socket type.

A socket type of `SOCK_RAW` bypasses the transport layer (TCP/UDP) and go
straight to the network layer (IP).
Hence `socket(AF_INET, SOCK_RAW, protocol)` needs the protocol to be specified.

There is no concept of port number (local or remote) on a raw socket, since
that's something the kernel does not control.

### Outgoing packets

Depending on the `protocol` passed to `socket(...)`, the data transmitted with
`send()` is:

- `IPPROTO_TCP`:  the full TCP packet (with headers)
- `IPPROTO_UDP`: the full UDP packet (with headers)
- `IPPROTO_RAW`: the full IP packet (with headers)

The kernel can add the IP header via the `IP_HDRINCL` socket option.
The kernel adds the header when the option is *not* set. In addition, the
kernel also takes care of setting the "protocol" field in the IPv4 header,
based on what protocol was specified to `socket()`.

- Socket protocol `IPPROTO_RAW` implies `IP_HDRINCL` being set.
- Socket protocol `IPPROTO_RAW` is send-only.

### Incoming packets

When receiving, we are *always* getting the full IP + TCP/UDP headers.

When a packet is received, it is passed to *any* raw sockets which have been
setup with the protocol of the packet. This is done before the packet is
passed to other protocols handlers.

## Block network for one process

- If you can control how to start the process, you can start it in a new
  network namespaces with no network interfaces.

- If you don't have control of the process, you can use cgroups + iptables:

```
mkdir /sys/fs/cgroup/net_cls/block
echo 42 > /sys/fs/cgroup/net_cls/block/net_cls.classid

iptables -A OUTPUT -m cgroup --cgroup 42 -j DROP

echo [pid] > /sys/fs/cgroup/net_cls/block/tasks
```

Unblock with:

```
echo [pid] >/sys/fs/cgroup/net_cls/tasks
```
