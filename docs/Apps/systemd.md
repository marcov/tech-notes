## systemd Unit Files

`Wants=`
If unit `foo.service` specifies `Wants=bar.service`, then:
- when `foo` is started also `bar` is started.
- if `bar` fails to start, this has no impact on `foo`
- this does not enforce a specific order

`Requires=`: similar to `Wants=`, but declares a stronger dependency.
If unit `foo.service` specifies `Requires=bar.service`, then:
- if `bar` fails to start, then `foo` will be stopped
- if `foo.service` specifies `After=foo.service` and `Wants=foo.service`, then
if bar fails to start, `foo` will NOT be started.

`Before=`, `After=` Ordering dependency
If unit `foo.service` specifies `Before=bar.service`, then:
- `bar.service` is delayed until `foo.service` is started
- When shutting down, the reverse dependency applies
