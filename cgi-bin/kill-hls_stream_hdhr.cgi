#!/bin/bash
# (c) 2021-03-05 Kelsie Flynn
# License MIT
#kill-hls_stream_hdhr.cgi
set -o posix
echo "Content-type: text/html"
echo ""
echo "<html>"
echo "<head>"
echo "<title>stop ffmpeg proc</title>"
#returning nests it until server refresh
echo "<meta http-equiv='refresh' content='2;url=/cgi-bin/ffmpegprocs.cgi'>"
echo "</head>"
echo "<body>"

#what host os?
#this sets up our CGIBIN_DIR and APACHE_USER
if [ $(uname) = 'Linux' ]; then
        #which apache or httpd?
        if [ -f /etc/debian_version ]; then
                echo "Debian based OS"
                echo "CGIBIN_DIR='/usr/lib/cgi-bin'"
                echo "APACHE_USER='www-data'"
                CGIBIN_DIR='/usr/lib/cgi-bin'
                APACHE_USER='www-data'
                echo "OS Test Passed"
        elif [ -f /etc/redhat-release ];then
                echo "RedHat based OS"
                echo "CGIBIN_DIR='/var/www/cgi-bin'"
                echo "APACHE_USER='apache'"
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

echo $APACHE_USER


ISRUNNINGPID='pgrep -x hls_stream_hdhr -u '$APACHE_USER' '
if [ ! -z $($ISRUNNINGPID) ];then 
	echo "HAS PID, $($ISRUNNINGPID), terminating it"
	#kill -n 9 $($ISRUNNINGPID) 2>/dev/null
	kill -n 15 $($ISRUNNINGPID) 2>/dev/null
else
	echo "no such PID to terminate"
fi

echo "</body></html>"

