License MIT</sub></sup>


### *This is not a real install script, just the steps from several parts strung together here until further long term integration.
#### installdebian10_steps.md
<br>
*Install simulation on Debian Netboot 10.7

<hr>

Update OS
```apt-get update -y && apt-get upgrade -y```

Add packages/add apache too if it isnt already installed
```apt-get install -y curl ffmpeg ffmpegthumbnailer git jq libnss-mdns unzip xmlstarlet```

enable cgi module for apache
```/sbin/a2enmod cgid```

In file : etc/apache2/mods-available/mime.conf
Under '<mime_module> uncomment the following :
```AddHandler cgi-script .cgi```

restart apache2
```systemctl restart apache2```

clone repo
```git clone https://github.com/ReallyJustAnotherBear/ShellCGI-SVR-HLS-HDHR```

#todo autoinstall
 ```su -s /bin/bash -c '/usr/lib/cgi-bin/INSTALL/PRE_install_COPYFILES.cgi' 'www-data'```


manual 

install files
```cp -av ShellCGI-SVR-HLS-HDHR/cgi-bin/* /usr/lib/cgi-bin/ ```

```cp -av ShellCGI-SVR-HLS-HDHR/html/* /var/www/html/ ```

Change the permissions on /cgi-bin to www-data
```chown -R www-data. /usr/lib/cgi-bin/*```

Change the permissions on /var/www/html to www-data
```chown -R www-data. /var/www/html```

change mode to 0755 for /var/www/html /usr/lib/cgi-bin
```chmod -R 0755 /var/www/html```
```chmod -R 0755 /usr/lib/cgi-bin```


Now you can exit the shell



Then from webbrowser go to :
```http://SERVER/cgi-bin/INSTALL/install.cgi```

Follow prompts from forms confirming settings, and
make sure to choose your FFmpeg Video Out default encoder/codec.
Use copy with hdhr-extend transcode models.
if you don't have a hardware h264 stream from a hdhr-extend transcode or one
of the others listed. Then chose 'libx264' which will be all software mode. 
After finished it will drop you back to SERVER/index.html
   ```


Try your webbrowswer to see if it works at SERVER/index.html without installing a native-hls extenstion.
Install the native hls extenstion if needed(not needed on MacOS/ios), firefox can use external players.

