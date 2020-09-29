# Docker / containerd

## Docker
### Get info using format string
List runtimes:
```
docker info --format "{{.Runtimes}}"
```

Get the path of a runtime:
```
 docker info --format "{{(index .Runtimes \"kata-runtime\").Path}}"
```

### Set the cgroup driver

Done in `/etc/docker/daemon.json`:

```
"exec-opts": ["native.cgroupdriver=systemd"]
```
## containerd

### Using `ctr`
#### Images
```
$ sudo ctr i pull docker.io/library/busybox:latest
$ sudo ctr images ls
```

#### Containers
```
$ sudo ctr run -t docker.io/library/busybox:latest foobar
$ sudo ctr containers ls
$ sudo ctr tasks ls
$ sudo ctr tasks kill -s KILL foobar
```

Events (from moby)
```
$ sudo ctr namespaces ls
$ sudo ctr --namespace moby events
```

