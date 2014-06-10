Pyramid Login Script
=============

A login system made using Pyramid

It uses bCrypt for password encryption. Please generate a unique 10 round salt and place it in /login/login/views.py before using this script on a live server. 

You can do this by running the following code:
```
import bcrypt

print bcrypt.gensalt(10)
```

Using the script
_____

Run the following command:
```
pserve production.ini
```

You will be able to visit the site at http://0.0.0.0:6543/

You can change this port in production.ini
