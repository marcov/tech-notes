# Procfs kernel internals

See:
- fs/proc/root.c
- fs/proc/base.c
  - `/proc/PID/exe`: `proc_exe_link(...) -> get_task_exe_file(task)`
  - `/proc/PID/root`: `proc_root_link(...)`
- fs/proc/array.c
