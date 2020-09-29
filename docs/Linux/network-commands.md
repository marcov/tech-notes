# Linux Network (iproute2) Commands

Manage network namespaces:
    $ ip netns

List nsid of the current network namespace
Obtained from netlink socket
    $ sudo ip netns list-id

New options of iproute2
    $ sudo ip netns list-id [target-nsid NSID] [nsid NSID]

List named network namespaces (/var/run/netns content)
    $ sudo ip netns list
    $ sudo ip netns monitor

Add network namespace
    $ sudo ip netns add NSNAME NSID

Move a network interface to another namespace
    $ sudo ip link set IFNAME netns  <NSNAME | NSID>

List interfaces in another network namespace
    $ sudo ip -netns NSNAME link show
    $ sudo ip netns exec NSNAME ip link show

Link type:
    $ sudo ip link show [type veth, bridge, macvlan, macvtap]

Show bridged eth devices:
    $ sudo bridge link show [dev DEVNAME]
    $ sudo bridge monitor

Inspecting Docker networking: docker network ls docker network inspect [NET NAME] # List network namespaces:
    $ lsns -t net
