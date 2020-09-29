# Seccomp

### Checking status
You can check if Seccomp is active is active for a specific process with:

```
grep Seccomp /proc/$PID/status
```

A value of 0 means deactivated, 2 means 'enforced'.

