# Apache2

## Redirect to an internal path
- Enable the Rewrite module
- Add to your config:
```
<Directory /var/www/>
...
    RewriteEngine On
    RewriteBase "/"
    RewriteRule "^index\.html$" "/new-path/new-index.html"
```
