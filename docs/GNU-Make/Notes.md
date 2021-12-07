## Notes on make

>
> Does updating file contents in a directory always update the timestamp make looks at?
>

These are two different questions. One is about make behaviour, the other is about
directory timestamps behaviour.

In general, make only looks at mtime.

Hence when a directory mtime changes, if that directory is a prerequisite,
then make will rebuild the target

When a directory mtime changes?
Not as intuitive as it seems: https://www.baeldung.com/linux/directory-last-modified-time#conclusion

TLDR:

| Action                                                           | mtime changes  |
| ------                                                           | ------         |
|Renaming myDir                                                    | No             |
|Changing myDir‘s Permission                                       | No             |
|Changing the content of files under myDir                         | No             |
|Adding, removing, or renaming files or subdirectories under myDir | Yes            |
