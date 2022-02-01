# Kernel misc

## Building deb kernel packages

See: https://wiki.debian.org/BuildADebianKernelPackage

```console
# default config:
make defconfig

# from an old config:
cp /boot/config-<...> .config
make oldconfig

# set some .config entries:
CONFIG_SYSTEM_TRUSTED_KEYS=""
CONFIG_SYSTEM_REVOCATION_KEYS=""

# build all the packages
nice make -j`nproc` bindeb-pkg
```
