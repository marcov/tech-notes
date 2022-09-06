# Linux/Unix Command Line Tools

## Misc Utils
- `ag`, `rg`, `ack`: better than `grep` for code
- `xdg-open`: open the GUI application associated to a file
- `cmp`: compare two files byte by byte

## cloud-image: set initial password
> NOTE: img can be a qcow2:

```
$ sudo virt-customize -a ubuntu-16.04-server-cloudimg-amd64-disk1.img --root-password password:linux
```

Or also:

```
# guestfish --rw -a <qcow2 image file name>
><fs> run
><fs> list-filesystems
><fs> mount /dev/vda1 /
><fs> vi /etc/shadow
```
#NOTE: REMOVE the `!!` from the file
```
><fs> umount /
><fs> exit
```

Or also:

```console
# modprobe nbd max_part=8 &&
# qemu-nbd -c /dev/nbd0 image.qcow2
# mount /dev/nbd0p1 /mnt
# chroot a sh -c "echo 'root:password' | chpasswd"
# umount /mnt
# qemu-nbd -d /dev/nbd0
```

## nohup: keep a command running even when the terminal is closed
```
$ nohup <command> <command options> &
```

Avoid generating nohup.log:
```
$ nohup <command> <command options> >dev/null &
```

## SED
### Delete lines
With a given pattern (`/pattern/d`):
```
$ sed "/pattern/d" file.txt
```

In a given range (`i,jd`):
```
$ sed "2,14d" file.txt
```

### Print only a given pattern found in a given line
Make sed print only relevant pattern.
E.g. only print the "..." part in the lines having the format "... bar". Do not
print lines not having this pattern.

```
sed -n 's/ \+bar//p'
```

## ss: socket statistics
```
$ ss --tcp
$ ss --udp
$ ss -plunt
```

## start-stop-daemon: daemonize a process
On regular Linux:
```
$ start-stop-daemon --start --oknodo --startas /root/usb/coredns --  -conf /root/usb/Corefile -pidfile /var/run/coredns.pid
```
On OpenWRT:
```
$ start-stop-daemon -S -b -x /root/usb/coredns --  -conf /root/usb/Corefile -pidfile /var/run/coredns.pid
```

## TMUX
### Copy lines into buffer:
`prefix` + `:`, type `capture-pane -S -<NUM OF LINES TO SAVE>`

### Save buffer to file:
`prefix` + `:`, type `save-buffer filename.txt`

### Move pane to a new window

While on current pane: `prefix :break-pane`

## update-alternatives
### Basic usage
```
$ sudo update-alternatives --display vi
$ sudo update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 99
$ sudo update-alternatives --install /usr/bin/vi vi /usr/bin/vim 100
$ sudo update-alternatives --config vi
$ sudo update-alternatives --remove-all vi
```

## xset: configure display features
### Query settings
```
$ xset q
```

### Enable DPMS
```
$ xset +dpms
```

### Force DPMS on
```
$ xset dpms force on
```

## rcconf
`rcconf`: configure startup services on Debian

## find
Execute a command for each result of `find`:

Either use `';'` or `\;`:
```
$ find /path -exec cmd1 '{}' ';'
```
Multiple commands are possible:
```
$ find /path -exec cmd1 '{}' ';' -exec cmd2 '{}' ';'
```

## Create a RAM disk
```
mount -t tmpfs -o size=512m tmpfs /mnt/ramdisk
```

## Specify a match group with grep
- `-P`: Perl-style regex
- `-o`: only print the match:
- (regext) `\K`: reset the starting point of the reported match.
  Any previously consumed characters are no longer included in the final match.

E.g.: make grep print ONLY the next word after 'foo', and nothing else:
```
$ grep -P -o 'foo \K[^ ]+'
```
Or, used `sed -n 's///p'` ...

## getent: low-level host name resolution tool (nslookup alternative)
> NOTE: getent can do much more: displays entries from databases, configured in
`/etc/nsswitch.conf`.

```
$ getent ahosts google.com
$ getent hosts localhost
```

## SSH

### SSH port forwarding
Use `ssh -L local-port:host-addr:host-port -N [-f]`.

- `-L local-port:host:host-port`: Forward the `local-port` TCP connection to the given
remote host:host-port. This makes ssh listen locally `local-port`

- `-N`: do not execute a command (because of `-L`)

- `-f`: go in background

### SSH VNC tunnel

1. Start the VNC server remotely:
```
$ vncserver
```

2. Setup the SSH tunnel locally:
```
$ ssh -L 5901:127.0.0.1:5901 -N -f -p SSH-PORT -l pi example.com
```

3. Run the VNC client locally:
```
$ xtigervncviewer
```

### Do not store host keys fingerprints to `~/.ssh/known_hosts`

```
Host 10.* 192.168.* 172.*
    UserKnownHostsFile /dev/null
    StrictHostKeyChecking no
```

NOTE: `Host` can be a single host, or a white space separated list. Use `*` to
define patterns.

## mtr - my tracerouter
`mtr` combines the functionality of the traceroute and ping programs in a single
network diagnostic tool.

## openssl cheats
See a certificate content:
```
$ openssl x509 -text -noout -in /PATH/TO/THE/CERT.crt
```
