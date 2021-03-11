#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#install.cgi
echo "Content-type: text/html"
echo ""
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<html>"
echo "<head>"
echo "<title>HLS Live Installer</title>"
echo "<style>"
echo ".button0 {color:black;background-color:red;width:50%;font-size:32px;padding:4px 2px;border-radius:24px;text-decoration:none}"
echo ".button {color:black;background-color:lime;font-size:64px;padding:1px 18%;border:2px solid black;text-decoration:none;border-radius:96px}"
echo "body {
  background-color: black;
  color: green;
}"
echo "h4 {text-align: center;}"
echo "p {text-align: center;}"
echo "div {text-align: center;}"
echo "</style></head>"
echo "<body>"
echo "<header>"
echo "</header>"
echo "<br>"
echo "<br>"
echo "<div>"
echo "<h4>Please ensure you have your apache CGI setup and running prior to starting</h4>"
echo " "
echo "<h4>If you have apache but CGI unconfigured this install will fail by doing nothing</h4>"
echo " "
echo ""
echo "<h4>dependencies:</h4>"
echo "<p><i>Please ensure you have ffmpeg,ffmpegthumbnailer,xmlstarlet installed prior to starting</i></p>"
echo "For debian based OS"
echo "<p>apt-get install ffmpeg ffmpegthumbnailer xmlstarlet</p>"
echo "For redhat based OS"
echo "<p>yum install ffmpeg ffmpegthumbnailer xmlstarlet</p>"

echo "<br>"
echo "When your ready."
echo '<form action="/cgi-bin/INSTALL/setuphdhr.cgi" method="post">
  <label for="HDHR_IP">Enter your HDHOMERUN IP</label><br>
  <input type="text" id="HDHR_IP.cgi" name="HDHR_IP" value=><br>
  <input type="submit" value="Submit">
</form>'

echo "</div>"
echo "</body></html>"

