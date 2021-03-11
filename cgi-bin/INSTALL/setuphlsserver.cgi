#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#setuphlsserver.cgi
echo "Content-type: text/html"
echo ""
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo '<meta http-equiv="refresh" CONTENT="0;url=/cgi-bin/INSTALL/install3.cgi">'
echo "<html>"
echo "<head>"
echo "<title> setup hls server ip/hostname</title>"
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


#what host os?
#this sets up our CGIBIN_DIR and APACHE_USER
if [ $(uname) = 'Linux' ]; then
        #which apache or httpd?
        if [ -f /etc/debian_version ]; then
                THISOS="Debian based OS"
                #echo "$THISOS"
		#echo "CGIBIN_DIR='/usr/lib/cgi-bin'"
                #echo "APACHE_USER='www-data'"
		CGIBIN_DIR='/usr/lib/cgi-bin'
                APACHE_USER='www-data'
                echo "OS Test Passed"
        elif [ -f /etc/redhat-release ];then
                THISOS="RedHat based OS"
                #echo "$THISOS"
		#echo "CGIBIN_DIR='/var/www/cgi-bin'"
                #echo "APACHE_USER='apache'"
		CGIBIN_DIR='/var/www/cgi-bin'
                APACHE_USER='apache'
                echo "OS Test Passed"
        else
                echo "Unknown Linux"
                echo "OS Test FAILED"
		echo "CANT SET CGIBIN_DIR and APACHE_USER"
                exit 1  
        fi
else
        echo "Unknown OS"
        echo "OS Test FAILED"
        exit 1  
fi

echo "Serverinfo"
echo $THISOS
echo $APACHE_USER
echo $CGIBIN_DIR



HLSSERVER="$CGIBIN_DIR/HLS_SERVER.cgi"

read CONTENT
#validation here needed
#grep then digit?
#or
#if [ "$CONTENT" == "[[:digit:]]" ]; then
#if [ "$CONTENT" == "192.168.1.218:8888" ]; then
#    echo "$CONTENT" > $HDHRIP
#fi

#when validated
#echo $VALIDCONTENT > $
echo $CONTENT > $HLSSERVER


echo "<h2>Thank you.</h2>"
echo "Serverinfo"
echo "<pre>$(cat $HLSSERVER)</pre>"
echo "<pre>$(echo $THISOS)</pre>"
echo "<pre>$(echo $APACHE_USER)</pre>"
echo "<pre>$(echo $CGIBIN_DIR)</pre>"
echo "</body></html>"

