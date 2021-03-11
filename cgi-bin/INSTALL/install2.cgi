#!/bin/bash
# License MIT
#install2.cgi
echo "Content-type: text/html"
echo ""
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<html>"
echo "<head>"
echo "<title>HLS Live Installer page2</title>"
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
echo "<br>"
echo "<p>Now add this Servers IP or Hostname/FQDN</p>"
echo "<p>Currently your ENV shows your server at:</p>"
echo "<pre>$(echo $SERVER_ADDR)</pre>"
echo "<p>If this is the correct IP, pre-entered the form below and click submit</p>"
echo "<p>If you don't want use ip address, enter its hostname/fqdn instead</pr>"
echo "<p>This will be your apache/cgi/ffmpeg live HLS_SERVER</p>"
echo '<form action="/cgi-bin/INSTALL/setuphlsserver.cgi" method="post">
  <label for="HLS_SERVER">ip hostname or fqdn</label><br>
  <br>
  <input type="text" id="HLS_SERVER" name="HLS_SERVER" value='$SERVER_ADDR'><br>
  <input type="submit" value="Submit">
</form>'

echo "</div></body></html>"
