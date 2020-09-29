# Grouping commands in list

`( cmd1; cmd2; )`

- **Executed in a sub-shell** environment.
    - e.g., `exit` as last command does not affect the main shell
- Variable assignments do not remain in effect.

`{ cmd1; cmd2; cmd3; }`

  - **Executed in the current shell** environment.
      - e.g., `exit` as last command makes the main shell exit
  - The **return status** is the exit status of the **last command** in the list.
  - { and } are reserved words, so they must be separated from the commands with
    a space.

