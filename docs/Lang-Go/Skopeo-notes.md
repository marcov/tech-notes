# Skopeo Notes

## Specify foreign architectures

Raspberry PI x32:
```
skopeo --override-arch arm --override-variant v7 inspect docker://busybox:latest
```

Raspberry PI x64:
```
skopeo --override-arch arm64 --override-variant v8 inspect docker://busybox:latest
```


## Running tests locally
```
SKOPEO_LOCAL_TESTS=1 go test -check.f Sync -test.timeout=10m -check.v -tags integration
```
