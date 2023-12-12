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

There is there is no concept of a port number (local or remote) on a raw
socket, since that's something out of control of the kernel.

### Outgoing packets

Given a protocol, the data transmitted with `send()` should be:

- `IPPROTO_TCP`:  the full TCP packet (with headers)
- `IPPROTO_UDP`: the full UDP packet (with headers)
- `IPPROTO_RAW`: the full IP packet (with headers)

Whether the kernel adds or not the IP header is controlled via the `IP_HDRINCL`
socket option. When not set, the kernel will add the header for you. In addition,
the kernel also takes care of setting the "protocol" field in the IPv4 header,
based on what protocol was specified to `socket()`.

Protocol `IPPROTO_RAW` implies `IP_HDRINCL` set.
Protocol `IPPROTO_RAW` is send-only.

### Incoming packets

When receiving, we are always getting the full IP + TCP/UDP headers.

When a packet is received, it is passed to any raw sockets which have been
bound to the packet protocol, before the packet being passed to other protocols
handlers.
