# VIM

## Generate a compilation database for YCM / ccls, ...

clang has built-in support for generating the `compile_commands.json`
Simply compile each file using the flag `-MJ file.o.json`. E.g., when compiling
using a Makefile, add to the CFLAGS `-MJ $@.json`

To coalesce all json file in a compile_commands.json file use:

```console
sed -e '1s/^/[\n/' -e '$s/,$/\n]/' output/**/*.o.json > compile_commands.json
```

Legacy:

- `bear`
- `compiledb make ...`

## vimdiff

```
]c               - advance to the next block with differences
[c               - reverse search for the previous block with differences
do (diff obtain) - bring changes from the other file to the current file
dp (diff put)    - send changes from the current file to the other file
zo               - unfold/unhide text
zc               - refold/rehide text
zr               - unfold both files completely
zm               - fold both files completely
```

## Paste yanked into command mode

`CTRL-r "`
(CTRL-r will show ", pressing " will change " into the yanked value)

## Save as sudo

```
:w !sudo tee %
```

## Insert with Visual block mode (<C-v>)

Use `Shift+i`, type your stuff (will only edit one line), <Esc> (will repeat to all
the other lines).

## Sroll keeping the cursor line on the same line

`<C-e>`: scroll down
`<C-y>`: scroll up

## Jump to a tag

`:ta TAG-NAME` (aka `tag`): jump to a tag, same as `CTRL-]`.

When there are many instances of the same tag and you need to pick one (e.g.
function declaration and definition):

- `:ts TAG-NAME` (aka `tselect`)
- `:tj TAG-NAME` (aka `tjump`)
- `g] TAG-NAME`
