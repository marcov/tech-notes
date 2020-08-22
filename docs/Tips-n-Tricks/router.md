## Enable TFTP server on mac

Path is /private/tftpboot
(chmod files to 777)
Start: sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist
Stop: sudo launchctl unload -F /System/Library/LaunchDaemons/tftp.plist


Local test:
tftp <local i/f ip>
binary
trace
verbose
get <filename>

## Redboot serial: make CTRL-C work
```
echo -e "\0377\0364\0377\0375\0006" >break.bin
sudo arping -f 192.168.1.254
sudo nc -D -vvv 192.168.1.254 9000 <break.bin
telnet 192.168.1.254 9000
```

## Allow inbound connection with VPN enabled

Fix routing to access http server on LEDE router when VPN is on:

echo 200 isp2 >> /etc/iproute2/rt_tables
ip rule add from <interface_IP> table isp2
ip route add default via <gateway_IP> dev <interface> table isp2
