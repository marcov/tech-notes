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
## REMOVE the `!!` from the file
```
><fs> umount /
><fs> exit
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
### Delete line with a given pattern
```
$ sed "/pattern/d" file.txt
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

## getent: low-level host name resolution tool (nslookup alternative)
> NOTE: getent can do much more: displays entries from databases, configured in
`/etc/nsswitch.conf`.

```
$ getent ahosts google.com
$ getent hosts localhost
```

## SSH VNC tunnel
```
$ ssh -L 5901:127.0.0.1:5901 -N -f -p PORT -l pi example.com
```
