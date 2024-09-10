# `socket.timeout()`

`socket.settimeout()` does not set a timeout in the kernel. The timeout is
handled by the Python runtime. As a result, at kernele level, the socket is
made non-blocking.

If you want a true kernel-level timeout, use `socket.setsockopt()`.

```python
from socket import *
import struct

TIMEOUT_S = 5

sk = socket(AF_INET, SOCK_DGRAM)
timeval_opt = struct.pack("@LL", TIMEOUT_S, 0)
sk.setsockopt(SOL_SOCKET, SO_RCVTIMEO, timeval_opt)

sk.bind(("1.2.3.4", 12345))
```
