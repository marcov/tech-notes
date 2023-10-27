# DNS Tools

## getent: low-level host name resolution tool

>
> NOTE: getent can do much more: displays entries from databases, configured in
> `/etc/nsswitch.conf`.
>

```
$ getent ahosts example.com
93.184.216.34   STREAM example.com
93.184.216.34   DGRAM
93.184.216.34   RAW
2606:2800:220:1:248:1893:25c8:1946 STREAM
2606:2800:220:1:248:1893:25c8:1946 DGRAM
2606:2800:220:1:248:1893:25c8:1946 RAW

$ getent ahosts localhost
127.0.0.1       STREAM localhost
127.0.0.1       DGRAM
127.0.0.1       RAW

$ getent hosts localhost
127.0.0.1       localhost
```

## host

Yet another DNS lookup tool.

Query for mx record:

```
$ host -t MX f5.com 1.1.1.1
```

## dig

DNS over UDP:

```
$ dig @1.1.1.1 +notcp google.com
```

DNS over TCP:

```
$ dig @1.1.1.1 +tcp google.com
```

