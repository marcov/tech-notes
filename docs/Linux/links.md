# Soft (Sym) and Hard Links

## Hardlink

- Acts as a reference counter on the data stored.
- Deleting the source does **not** delete the content.
- Source and hard link have the same inode #.
- A hard link can't be dangling.
- Hard link needs to be on the same filesystem.
- Can't hard link to a directory.

## Symlink

- Like a file shortcut.
- Have a separate inode.
- Removing the symlink does not delete the original file.
- A symlink can be dangling if the source is deleted.
- Can span across filesystems.
