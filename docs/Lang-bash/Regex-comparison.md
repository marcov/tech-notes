# Regex comparisons

> **NOTE**: do not use " " (quotes) for the regex pattern!

```
if [[ "compare this         text with" =~ ^c.+ this\ +text with$ ]]; then
  echo "it's matching"
fi
```

> **NOTE2**: in some cases the pattern have to be put in a variable

E.g.
```
pattern="\<word\>"

[[ "there's a word in between" =~ $pattern ]] && echo matched
```
