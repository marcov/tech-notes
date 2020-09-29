# SUSE OSC Command line tool

## Have artifacts from another project available in my project
```
osc aggregatepac $other_project $(PKGNAME) $my_project
```

## Delete a package
```
osc rdelete $project $(PKGNAME)
```

## Revert to a previous revision
```
osc sr -r $rev $prj $package $prj -m "revert to $rev"
osc sr accept <id_given>
osc up
```

## Get the GPG public key for a $project on OBS
```
osc signkey $project > proj.key
```

## Get the key fingerprint
```
gpg --import --import-options show-only proj.key
```

