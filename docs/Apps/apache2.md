# Apache2

## Redirect to an internal path
- Enable the Rewrite module
- Add to your config:
```
<Directory /var/www/>
...
    RewriteEngine On
    RewriteBase "/"

    # Always redirect index to weather
    RewriteRule "^index\.html$" "/weather/index.html"

    # Condition: file / directory does not exist on disk.
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d

    # If condition is met, redirect everything to /weather
    RewriteRule . /weather
```
