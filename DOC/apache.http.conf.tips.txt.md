Apache configuration tips:

*All or some may or may not be needed. I haven't fully tested.


Under doc root dir I added:
```
Options +Indexes +FollowSymLinks
```


In the alias_module section:
```
ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
```



Add the following to logging section of your http.conf
```
ScriptLog "/var/log/httpd/script_error_log"
```

On debian: /etc/apache2/mods-available/mime.conf
Under mime_module:
```
AddHandler cgi-script .cgi .py
```
