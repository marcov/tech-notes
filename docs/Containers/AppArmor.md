# AppArmor

## Listing AppArmor features available in the kernel
There's a folder for each feature in `/sys/kernel/security/apparmor/features/`.

## Write a demo profile
### Profile for a specific executable
```
#include <tunables/global>

/usr/bin/mycommand {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  #include <abstractions/user-tmp>

  capability net_raw,
  capability setuid,
  capability setgid,
  capability dac_override,
  network raw,
  network packet,

  # for -D
  capability sys_module,
  @{PROC}/bus/usb/ r,
  @{PROC}/bus/usb/** r,

  # for -F and -w
  audit deny @{HOME}/.* mrwkl,
  audit deny @{HOME}/.*/ rw,
  audit deny @{HOME}/.*/** mrwkl,
  audit deny @{HOME}/bin/ rw,
  audit deny @{HOME}/bin/** mrwkl,
  @{HOME}/ r,
  @{HOME}/** rw,

  /usr/sbin/mycommand r,
}
```

### Profile suitable to be loaded at run time
```
#include <tunables/global>
profile demo-profile flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  deny mount,
  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/efi/efivars/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

## Loading a profile
```
$ sudo apparmor_parser -r -W /path/to/demo-profile
```

## Remove a profile
```
$ sudo apparmor_parser -R /etc/apparmor.d/profile.xyz
```

## Disable a profile
```
$ sudo ln -s /etc/apparmor.d/profile.xyz /etc/apparmor.d/disable/
```

## Apply a profile at runtime
```
$ echo "exec demo-profile" > /proc/self/attr/exec
```
