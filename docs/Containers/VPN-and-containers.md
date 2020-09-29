# VPN inside Containers

## Method 1: OpenVPN on host

1. Start the OpenVPN client
```
sudo /usr/sbin/openvpn --config <config name>
```


OpenVPN should have set up a new tun# device with its own IP address.

2. Set up a new docker network
```
sudo docker network create docker-vpn0 --subnet 10.193.0.0/16
```

3. Set up host routes so that the traffic from the new docker network is routed thru the tun device

```
sudo ip route add default via <tun if IP address> table 200
sudo ip rule add from 10.193.0.0/16 table 200
```

4. Set up reverse path fitlering
```
# rp_filter is reverse path filtering. By default it will ensure that the
# source of the received packet belongs to the receiving interface. While a nice
# default, it will block data for our VPN client. By switching it to '2' we only
# drop the packet if it is not routable through any of the defined interfaced.
sysctl -w net.ipv4.conf.all.rp_filter=2
```

5. Ready to go
```
docker run -it --rm --net=docker-vpn0 alpine

# Check your IP with:

alpine:/# curl http://httpbin.org/ip
```

## Method 2: OpenVPN in a container

T.B.D.
