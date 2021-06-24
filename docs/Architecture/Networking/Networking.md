## Ephemeral Ports

This is the range of ports that is not part of the well-known ports.
When a process calls connect(2) without binding to a specific port, it is assigned
a source port from the ephemeral port range. On Linux the range is specified in
`/proc/sys/net/ipv4/ip_local_port_range`.
