# macOS
##Shortcuts
- `Command - m`: minimize a window
- `Command - Tab` + (select application) + `(release tab)` + `Option` + `(release Command)`:
un-minimize an application window

## X11 forwarding
1. Install XQuartz client on mac
2. Make sure xauth is set up in `/etc/ssh/ssh_config` (should be done automatically by XQuartz)
3. Add a very long forward time out

```
Host *
    XAuthLocation /opt/X11/bin/xauth
    # Do not timeout X11 forwarding
    ForwardX11Timeout 596h
```

## Prevent sleeping
```
$ pmset noidle
```

## Fix early 2011 MBP
- Boot Live USB Linux with cmdline:
```
module_blacklist=radeon,radeonfb
```

- Easiest thing to do is to do this changes to the file system from another mac,
since you may not be able to boot in recovery mode at all!
    * `rm -rf /System/Library/Extensions/*{ATI,AMD}*/*`: keep the directories but make
    sure they are empty. This allows to boot normally without the NVRAM hack below!
    * `rm -rf /System/Library/Caches/com.apple.kext.caches`
    * `mkdir /System/Library/Caches/com.apple.kext.caches`
    * `touch /System/Library/Extensions`
- `$ sudo nvram fa4ce28d-b62f-4c99-9cc3-6815686e30f9:gpu-power-prefs=%01%00%00%00`:
if you can't boot normally, boot in single-user mode (Command-s)
- Reboot

## Increase keyboard repeat rate
Max out keyboard repeat rate:
```
defaults write -g InitialKeyRepeat -int 10 # normal minimum is 15 (225 ms)
defaults write -g KeyRepeat -int 1 # normal minimum is 2 (30 ms)
```
