# Cross Compilation
Just set the env vars `GOARCH`, `GOOS`. E.g.:

```
GOOS=linux GOARCH=arm go build #Any options normally used to build...
```

This will build for ARMv7L.
