# Deb Packages

### Get package from file name / path
```
$ dpkg --search <some-name>
$ dpkg --search <filepath>
OR
$ dpkg-query --search ...
```


### List files in a package
```
$ dpkg-query --listfiles <package-name>
# OR
$ dpkg --list-files <package-name>

```

### Get (installed) package name matching a pattern
```
$ dpkg-query --show <pattern>
```

### Get all installed packages
```
$ dpkg-query --show
# OR
$ dpkg-query --list
# OR
$ apt list
```
