# Rpm Packages

### Extract RPM package
```
rpm2cpio <pkg>.rpm | cpio -idmv
```

### Check package integrity
```
rpm -K --nosignature <rpm-file>
```

### Check package signature
```
rpm -K --nosignature <rpm-file>
```

### Show the RPM signing key trusted on your system
```
rpm -qa "gpg-pubkey*" --qf "%{version}-%{release} %{summary}\n"
```

### Get details about a signing key:
```
rpm -qi gpg-pubkey-12345-6789
```

## RPM spec files
## Macros
- `%{?the_variable}` : if `the_variable` is not defined, this is replaced with an empty string
- `0%{?the_variable}` : if `the_variable` is not defined, this is replaced with `0`

## Multiple conditions in `%if`
You can use round parenthesis:

```
%if 0%{?other_version} >= 11 || ( 0%{?is_foo} && 0%{?foo_version} >= 10 )
```

## Evaluate some spec file content
- Create a dummy spec file, and then call:
 * `rpmbuild -ba dummy.spec`
 * `rpmbuild -bp dummy.spec` : only go thru %prep

- From command line:
`rpm --eval 'Foo: %{?foo_variable}'`
