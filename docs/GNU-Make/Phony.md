# Some notes about `.PHONY` targets
From GNU Make manual:

A phony target should not be a prerequisite of a real target file; if it is,
its recipe will be run every time make goes to update that file. As long as a
phony target is never a prerequisite of a real target, the phony target recipe
will be executed only when the phony target is a specified goal (see Arguments
to Specify the Goals).

