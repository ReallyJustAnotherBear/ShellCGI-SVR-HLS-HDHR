#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#quicksetup.cgi
echo "Content-type: text/html"
echo ""
echo "<html><head></head><body>"
#set -e
if [ $# -eq 0 ]; then
    echo " "
    echo "No arguments provided, Use: your hdhr fqdn/hostname or ip as the first argument, and port too if not the standard port 80"
    echo "eg. use "
    echo " "
    echo "./quicksetup HDHR_HOSTNAME_OR_IP "
    echo " "
    echo "eg for a HDHR with ip:192.168.1.218"
    echo " "
    echo " ./quicksetup 192.168.1.218"
    echo " "
    exit 1
fi

if [ $(id -un) != 'www-data' ]; then
	if [ $(id -un) != 'apache' ]; then
		echo "exiting, only run this script as www-data or apache user"
		exit 1
	fi
fi

echo "Running as user=$(id -un)"
echo "Okay. User check passed"

HDHR_IP=$1         #enter your fqdn/ip here, append any custom port you might have as well if not on port 80.

#prelaunch check
[[ "$(command -v bash)" ]] || { echo "bash is not installed" 1>&2 ; exit 1; }

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

if [ -x /usr/bin/xmlstarlet ];then
	curl  -s http://$HDHR_IP/lineup.xml|xmlstarlet sel -T -t -v "//GuideNumber" -n > /var/www/html/channels.txt
else
    echo "xmlstarlet not found at /usr/bin/xmlstartlet, exiting"
    exit 1
fi

#validate and rewrite /var/www/html/channels.txt
#validate our channels work here with good returns from ffprobe before adding
#else we can end up with channels that will not tune in our channels.txt and result in failures later.
#filter 1, run through '*digit.digit' filter
#rewrite
#run through ffprobe basic test and exclude non zero result channels

#create directories from channels.txt

if [ -d /var/www/html ]; then 
	echo "html dir found in /var/www"
	if [ -d /var/www/html/hls ] && [ -f /var/www/html/channels.txt ]; then 
		cd /var/www/html/hls
		echo "hls dir found in /var/www/html and we have a channels.txt"
		echo " "
		echo "creating any missing direcories from channels.txt"
		for i in $(cat /var/www/html/channels.txt);do 
			if [ ! -d $i ];then
			     mkdir -v /var/www/html/hls/$i
			fi
		done
		echo "listing channel directories"
		echo "ls -alv /var/www/html/hls/"
		ls -alv /var/www/html/hls/
		exit 0
	else
	
		echo "We have html but hls NOT dir found in /var/www/html"
		echo "Creating hls dir in  /var/www/html"
		mkdir -v /var/www/html/hls; cd /var/www/html/hls
		echo "creating any missing direcories from channels.txt"
		for i in $(cat /var/www/html/channels.txt);do 
			if [ ! -d $i ];then
			     mkdir -v /var/www/html/hls/$i
			fi
		done
		echo "listing channel directories"
		echo "ls -alv /var/www/html/hls/"
		ls -alv /var/www/html/hls/
		exit 0
	fi
else
	echo "Directory /var/www/html doesnt exist exiting"
	exit 1
fi
echo "</body></html>"
