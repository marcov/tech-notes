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
mkdir /sys/fs/cgroup/net_cls/blocked-network
echo 42 > /sys/fs/cgroup/net_cls/blocked-network/net_cls.classid

iptables -A OUTPUT -m cgroup --cgroup 42 -j DROP

echo [pid] > /sys/fs/cgroup/net_cls/blocked-network/tasks
```

Unblock with:

```
echo [pid] >/sys/fs/cgroup/net_cls/tasks
```

### Limit interface bandwidth with tc

```
# Add limit
tc qdisc add dev ens33 root slowdown delay 1000ms

# Remove limit
tc qdisc del dev ens33 root netem
```

## Iptables

- Five independent **Tables** (specify table with `-t`)
- Each table have built-in chains + user defined chains
- Each chain have a list of rules, matching a set of packets

Tables:
- `filter`: default.
  Chains:
  * INPUT (pkts for local sockets)
  * FORWARD (pkts routed)
  * OUTPUT (locally generated pkts)

- `nat`: pkts creating a new connection. Used to alter pkts
  Chains:
  * PREROUTING (coming in pkts)
  * INPUT
  * OUTPUT
  * POSTROUTING (leaving pkts)

- `mangle`: specialized pkts altering

- `raw`: ...

- `security`: MAC rules

## NAT

https://www.karlrupp.net/en/computer/nat_tutorial

## Rate limit input connections

If more than `$dropConnCount` connection attempts are made in `$dropConnInterval`
seconds, drop them.

```sh
    declare -i dropConnCount=3
    declare -i dropConnInterval=240

    echo "INFO: iptables delete chain LOGDROP"
    iptables --zero INPUT
    iptables --flush INPUT
    iptables --zero LOGDROP
    iptables --flush LOGDROP
    sleep 1
    iptables --delete-chain LOGDROP || { echo "WARN: delete chain LOGDROP failed"; }

    echo "INFO: iptables new chain LOGDROP"
    iptables -N LOGDROP

    echo "INFO: iptables append LOGDROP: jump LOG"
    iptables -A LOGDROP -j LOG

    echo "INFO: iptables append LOGDROP: jump DROP"
    iptables -A LOGDROP -j DROP

    echo "INFO: iptables insert INPUT (match recent)"
    iptables -I INPUT -p tcp --dport 22222 -i eth0 -m state --state NEW -m recent --set

    echo "INFO: iptables insert INPUT (match recent): jump LOGDROP"
    iptables -I INPUT -p tcp --dport 22222 -i eth0 -m state --state NEW -m recent --update --seconds $dropConnInterval --hitcount $dropConnCount -j LOGDROP
```
