# Procfs kernel internals

See:
- fs/proc/root.c
- fs/proc/base.c
  - `/proc/PID/root`: `proc_exe_link(...) -> get_task_exe_file(task)`
  - `/proc/PID/exe`: `proc_root_link(...)`
- fs/proc/array.c
