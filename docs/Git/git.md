# Git

## Show diff between a revision and its parent

These two commands are equivalent:

```
$ git diff <REV>^!
$ git diff <REV>~..<REV>
```

## Show diff between different files in different branches

```
git difftool -d REV1:path/to/file1 REV2:path/to/another/file2
```

## Difference between `..` and `...`

`..`: used with `git log`

E.g.:
```
$ git log r1..r2
```

means "list of commits logs in branch r2, but exclude commits in r1"
Useful when r2 is a branch of r1.

`...`: used with `git diff`
E.g.
```
git diff r1...r2
```
means "show diff in BOTH r1 and r2 from the common ancestor of r1 and r2"

## Create a patch from a commit / apply it
Create patch e.g. from the last commit:
```
$ git format-patch -1 HEAD
```

Apply patch with:
```
$ git am < file.patch

$ git am --3way 000x-...-file.path
```

Use `--3way` to generate 3-way diff stuff when patching fails.

## rev-parse
Get (short) commit hash of `HEAD`
```
$ git rev-parse HEAD

$ git rev-parse --short HEAD
```

## Pull from a forced update (push --force)
```
$ git stash # if needed
$ git fetch
$ git reset remote/branch --hard
$ git rebase -i remote/branch
```

## GitHub: checkout a PR locally
Given a PR identified by ID, you can fetch it a local branch with name `<branch-name>`

>NOTE: `<local-branch>` can be any name!

```
$ git fetch origin pull/<PR ID>/head:<local-branch>

$ git checkout <branch-name>
```

If doing any modification, you can also push with:
```
git push origin <branch-name>
```

## Git `describe`
Find the most recent tag that is reachable from a commit:
```
$ git describe [<commit id>]
```
When no commit id is given, default is HEAD.

Output:
```
<tag name>-<number of commits since last tag>-<most recent commit id>
```

## Add single hunks interactively
```
$ git add -i
```
- Then pres `4`

OR just:
```
$ git add --patch
```

## Git rebase

Use `rebase` for:

- `git rebase -i master`: move a set of commits on the top, instead of merging.
- `git rebase -i COMMIT-ID`: edit/squash a set of commits (pick, drop, reword commit message, squash).
- To rebase from a common ancestor, use `git merge-base HEAD master`

```
$ git pull --rebase <mybranch>
```

`--autosquash`: automatically set a `fixup!` commit to be a fixup instead of a pick.
Can be enabled by default with the config: `rebase.autoSquash`

See: https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase

## Manage submodules
Add submodules to existing repo:
```
$ git submodule add https://github.com/foo/bar.git
```

Clone a repo and at the same time populate submodules:

During clone:
```
$ git clone XXXX --recursive
```

Or after cloning:

```
$ git submodule update --init --recursive
```

## Amend: edit the last commit message OR add new changes to last commit
```
$ git commit --amend <filename>
```

See: https://www.atlassian.com/git/tutorials/rewriting-history

## Specifying a Git revision
`HEAD`: most recent commit in the current branch

`<REV>`, `<REV>~0`, `<REV>^0`: the revision itself

`<REV>~`, `<REV>~1`: previous commit of revision `<REV>` (if multiple parents, 1st parent)

`<REV>~n`: previous n commit of revision <REV>

`<REV>^`, `<REV>^1`: 1st parent of `<REV>`

`<REV>^n`: nth parent of `<REV>`

`<REV>^!`: equivalent to `<REV>~..<REV>`

`git rev-parse` for more info!

## Delete sensitive data
Use the bfg tool

```
$ bfg --replace-text sensitive_text_list.txt
```

NOTE: if hosting remotely (e.g. GitHub), the remote repo need to be deleted and re-created!

## Undo the last commit
(But keep changes)
```
$ git reset HEAD~
```

## Unstage staged / added files
(But keep changes)
```
$ git reset HEAD
```

## Show

### Show changes done in a commit

Equivalent to `git difftool -d REVISION^!`:
```
$ git show REVISION
```

### Show a specific file revision
```
$ git show REVISION:./path_of_file
```

## Delete a branch
First, check out any branch != branch_to_delete:
```
$ git checkout master

$ git branch -d branch_to_delete

$ git push origin --delete branch_to_delete
```

Remove any remote tracking branches that no longer exist remotely:
```
$ git fetch --prune
```

## Push from a local branch to another upstream branch
ID can be `HEAD`, a branch name, a commit hash, ... :

```
$ git push [remote-name] <ID>:<upstream-branch-name>
#                            ^
#                            |____ use ":"

$ git branch --contains=HEAD
foo
# Push HEAD in foo to remote branch bar
$ git push origin HEAD:bar
# Push branch foo to remote branch bar
$ git push origin foo:bar
```
## Common ancestor
Find as good common ancestors as possible for a merge:
```
$ git merge-base COMMIT1 COMMIT1
```
Handy to be used with rebase:
```
$ git rebase -i $(git merge-base HEAD origin/master)
```

## **Really** clean everything

>
> **NOTE**: USE WITH CARE!
>
```
$ git clean -dffx
```

## Checkout a branch with an arbitrary name
```
$ git checkout -b LOCAL-BRANCH origin/remote-branch-name
```

## Ignore files without changing `.gitignore`

Just add those files to `$GIT_DIR/info/exclude`.

## Prevent changes to a tracked file to show up in `git status`
Add this to your config:
```
[alias]
  ignore = update-index --assume-unchanged
  unignore = update-index --no-assume-unchanged
  ignored = "!git ls-files -v | grep ^[a-z]"
```

and use `git ignore changed-file`

## Fetching an untagged (orphaned) commit ID

Git does not fetch orphaned commit IDs, i.e IDs not reachable by name.
You first need to tag tag commit ID upstream.

## Fetch & update local branch
This way, you don't need to `git checkout` and `git pull`.
```
$ git fetch origin BRANCH-NAME:BRANCH-NAME
```

## Rewrite previous commits username and emails

Via this `change-commits` alias:
```
git config --global alias.change-commits '!'"f() { VAR=\$1; OLD=\$2; NEW=\$3; shift 3; git filter-branch --env-filter \"if [[ \\\"\$\`echo \$VAR\`\\\" = '\$OLD' ]]; then export \$VAR='\$NEW'; fi\" \$@; }; f"
```

E.g., change the author:
```
git change-commits GIT_AUTHOR_NAME "old name" "new name"
```

change email for the last 10 commits:
```
git change-commits GIT_AUTHOR_EMAIL "old@email.com" "new@email.com" HEAD~10..HEAD
```

List of commit envs:

```
GIT_AUTHOR_NAME is the human-readable name in the “author” field.

GIT_AUTHOR_EMAIL is the email for the “author” field.

GIT_AUTHOR_DATE is the timestamp used for the “author” field.

GIT_COMMITTER_NAME sets the human name for the “committer” field.

GIT_COMMITTER_EMAIL is the email address for the “committer” field.

GIT_COMMITTER_DATE is used for the timestamp in the “committer” field.
```

## Clone

- Only a single branch or tag: use `--single-branch --branch <BRANCH-NAME | TAG-NAME>`

- Shallow clone: use ` --depth`. E.g. `--depth 1` will only clone the latest revision.

Combined:

```
git clone \
  --depth 1 \
  --branch Ubuntu-aws-5.4-5.4.0-1041.43_18.04.1 \
  --single-branch \
  git://git.launchpad.net/~canonical-kernel/ubuntu/+source/linux-aws/+git/bionic
  DEST-FOLDER
```

## Switch to branches
You can use `git switch BRANCH-NAME` instead of `git checkout ...`.

## Restore files
You can use `git restore --file ./PATH/TO/FILE` instead of `git checkout -- ./PATH/TO/FILE`.

## Stash
You can stash only staged changes with `git stash --staged --message "only stashing staged stuff"`.

## Jump
You can use the `git-jump` extension to jump to interesting stuff in an editor:
- merge: `git jump merge [-- file/path]`
- diff
- grep

## Fancy diff
Use `--color-words` option to show changed words in a line in red / green color,
instead of seeing the same line before / after the change.

## Short status
`git status -s`
