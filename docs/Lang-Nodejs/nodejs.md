# Node.js

### Run a script continuously
A simple CLI tool for ensuring that a given script runs continuously (i.e. forever).
```
$ npm install forever -g
$ forever start app.js
```

### New project template
Generate an http site template:
```
$ npm install express-generator -g
$ express —-view pug projectname
```
```
$ cd projectname/
```

Install all the dependencies:
```
$ npm install
```

Initialize the npm project:
```
$ npm init
```

Run node to serve the website (you WILL need to kill & restart every time source code is changed!):
```
$ DEBUG=projectname:* npm start
```

Alternatively to npm start, use nodemon to AUTOMATICALLY restart node server every time source code is changed:
```
$ npm install nodemon
$ DEBUG=projectname:* nodemon
```

Be sure `bin/www` line:
```
var debug = require('debug')('projectname:server');
```
is set to the correct `projectname` to get all debug traces!
