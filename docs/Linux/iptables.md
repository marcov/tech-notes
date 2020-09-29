# Iptables

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
