# Coding hints

### Locals initialization
Do not initialize auto variables at the top of a function for no reasons.

This could prevent a static analyzer to catch a "use without initialize" bug,
if when writing the code we expect the variable to always be initialized.

### Switch-case over an enum (C++)
When doing switch case over an enum, avoid having a `default:`.
Better to explicitly list all of the `case` value instead.
This way if you add a new enum value, you will get a compiler error when building
the code, complaining that a `case <newvalue>` is missing.
