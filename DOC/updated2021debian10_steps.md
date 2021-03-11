License MIT</sub></sup>


### *This is not a real install script, just the steps from several parts strung together here until further long term integration.
#### installdebian10_steps.md
<br>
*Install simulation on Debian Netboot 10.7
<hr>

Update OS
```apt-get update -y && apt-get upgrade -y```

Add packages/add apache too if it isnt already installed
```apt-get install -y curl ffmpeg ffmpegthumbnailer git libnss-mdns unzip xmlstarlet```

enable cgi module for apache
```/sbin/a2enmod cgid```

restart apache2
```systemctl restart apache2```

clone repo
```git clone https://github.com/kelsieflynn/CGI-SERVER-HLS-HDHR```

install files
```cp -av CGI-SERVER-HLS-HDHR/cgi-bin/* /usr/lib/cgi-bin/ ```

```cp -av CGI-SERVER-HLS-HDHR/html/* /var/www/html/ ```

Change the permissions on /cgi-bin to www-data
```chown -R www-data. /usr/lib/cgi-bin/*```

Change the permissions on /var/www/html to www-data
```chown -R www-data. /var/www/html```

change mode to 0755 for /var/www/html /usr/lib/cgi-bin
```chmod -R 0755 /var/www/html```
```chmod -R 0755 /usr/lib/cgi-bin```

In file : etc/apache2/mods-available/mime.conf
Under '<mime_module> uncomment the following :
```AddHandler cgi-script .cgi```


Then from webbrowser go to :
```http://SERVER/cgi-bin/INSTALL/install.cgi```

When promted from forms:
  
    Enter your hdhr device IP in ipv4 format and choose submit.
    Enter your HLS server IP or hostname and choose submit.
    Choose your FFmpeg Video Out default encoder/codec
      if you don't have a hardware h264 stream from a hdhr-extend transcode or one
      of the others listed. Then chose 'libx264' which will be all software mode. 
    After finished it will drop you back to SERVER/index.html


### Temporary actions to complete install until integration
   
Now as root usr run quicksetup.cgi as the apache user(www-data) against your HDHR IP
 Replacing my ip '192.168.1.218' with your hdhr ip
 ```su -s /bin/bash -c '/usr/lib/cgi-bin/INSTALL/quicksetup.cgi 192.168.1.218' 'www-data'```
       
   a good run should be similar to:
   ```
           Content-type: text/html
      
          <html><head></head><body>
           Running as user=www-data
           Okay. User check passed
           Debian based OS
           CGIBIN_DIR='/usr/lib/cgi-bin'
           APACHE_USER='www-data'
           OS Test Passed
           html dir found in /var/www
           hls dir found in /var/www/html and we have a channels.txt

            creating any missing direcories from channels.txt
            mkdir: created directory '/var/www/html/hls/13.1'
            mkdir: created directory '/var/www/html/hls/13.2'
            mkdir: created directory '/var/www/html/hls/13.3'
            mkdir: created directory '/var/www/html/hls/16.1'
            mkdir: created directory '/var/www/html/hls/16.2'
            mkdir: created directory '/var/www/html/hls/16.3'
            mkdir: created directory '/var/www/html/hls/23.1'
            mkdir: created directory '/var/www/html/hls/23.2'
            mkdir: created directory '/var/www/html/hls/34.1'
            mkdir: created directory '/var/www/html/hls/34.2'
            listing channel directories
            ls -alv /var/www/html/hls/
            total 48
            drwxr-xr-x 12 www-data www-data 4096 Jan 15 14:44 .
            drwxr-xr-x  3 www-data www-data 4096 Jan 15 14:41 ..
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 13.1 
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 13.2
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 13.3
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 16.1
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 16.2
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 16.3
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 23.1
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 23.2
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 34.1
            drwxr-xr-x  2 www-data www-data 4096 Jan 15 14:44 34.2
   ```



   now finish up by creating channel links 
   
   ```su -s /bin/bash -c '/usr/lib/cgi-bin/INSTALL/createChannelLinks.cgi' 'www-data'```


   here's a good run example
   
   ```
      Content-type: text/html

      <html><head></head><body>
      You already have Channels:
      <pre> </pre>
      <pre>13.1
      13.2
      13.3
      16.1
      16.2
      16.3
      23.1
      23.2
      34.1
      34.2</pre>
      Backing up old /var/www/html/channels.txt to /var/www/html/channels.txt.OLD
      <pre>'/var/www/html/channels.txt' -> '/var/www/html/channels.txt.OLD'</pre>
      <pre>/var/www/html/channels.txt.OLD</pre>
      CGI_BINDIR = /usr/lib/cgi-bin
      going to CGI_BINDIR
      <br>
      finding old channels links, if any, that point to channelcmd.template.cgi and removing them
      <pre>find -samefile channelcmd.template.cgi</pre>
      <pre>./channelcmd.template.cgi</pre>
      <br>
      <pre></pre>
      <pre>./channelcmd.template.cgi</pre>
      Creating new links from channels.txt
      <pre>'13.1.cgi' => 'channelcmd.template.cgi'
      '13.2.cgi' => 'channelcmd.template.cgi'
      '13.3.cgi' => 'channelcmd.template.cgi'
      '16.1.cgi' => 'channelcmd.template.cgi'
      '16.2.cgi' => 'channelcmd.template.cgi'
      '16.3.cgi' => 'channelcmd.template.cgi'
      '23.1.cgi' => 'channelcmd.template.cgi'
      '23.2.cgi' => 'channelcmd.template.cgi'
      '34.1.cgi' => 'channelcmd.template.cgi'
      '34.2.cgi' => 'channelcmd.template.cgi'</pre>
      <br>
      Channel Links:
      <pre> </pre>
      <pre>./13.1.cgi
      ./13.2.cgi
      ./13.3.cgi
      ./16.1.cgi
      ./16.2.cgi
      ./16.3.cgi
      ./23.1.cgi
      ./23.2.cgi
      ./34.1.cgi
      ./34.2.cgi
      ./channelcmd.template.cgi</pre>
      </body></html>
   ```


Now you can exit the shell

You try your webbrowswer to see if it works at SERVER/index.html without the native-hls extenstion.
Install the native hls extenstion if needed 

I'll tie all this together soon for a pure web install.
