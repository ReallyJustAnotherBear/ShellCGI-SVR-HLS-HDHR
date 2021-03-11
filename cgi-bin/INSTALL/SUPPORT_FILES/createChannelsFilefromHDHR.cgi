#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#createChannelsFilefromHDHR.cgi
#check for programs/cmds/utilities to be used here first or exit and suggest
#check for xmlstarlet, if ok, continue, else suggest they install with apt/yum package mgr, then exit 1

#add hdhr specific check for scanned channels
#add hdhr specific scan channels if not
#download channels from hdhr
#add channels to $CHANNELS location
#old template for creating links below
echo "Content-type: text/html"
echo ""
echo "<html><head></head><body>"
CHANNELS=/var/www/html/channels.txt
if [ -s $CHANNELS ];then
	echo "You already have Channels:"
	echo "<pre> </pre>"
	echo "<pre>$(cat $CHANNELS)</pre>"
	echo "Backing up old $CHANNELS to $CHANNELS.OLD"
	echo "<pre>$(cp -v $CHANNELS $CHANNELS.OLD)</pre>"
	echo "<pre>$(echo $CHANNELS.OLD)</pre>"
	#check cgi-bin dir location and set
	if [ -s /usr/lib/cgi-bin ];then 
		CGI_BINDIR="/usr/lib/cgi-bin"
		echo "CGI_BINDIR = $(echo $CGI_BINDIR)"
		echo "going to CGI_BINDIR"
		cd $CGI_BINDIR
		echo "<br>"
		echo "finding old channels links, if any, that point to channelcmd.template.cgi and removing them"
		echo "<pre>find -samefile channelcmd.template.cgi</pre>"
		echo "<pre>$(find -samefile channelcmd.template.cgi -print|sort)</pre>"
		echo "<br>"
		echo "<pre>$(find .  -type f -name '[[:digit:]]*'.cgi -exec rm {} \;)</pre>"
		echo "<pre>$(find -samefile channelcmd.template.cgi -print|sort)</pre>"
		echo "Creating new links from channels.txt"
		echo "<pre>$(for i in $(cat /var/www/html/channels.txt);do ln -v channelcmd.template.cgi $i.cgi ; done)</pre>"
		echo "<br>"
		echo "Channel Links:"
		echo "<pre> </pre>"
		echo "<pre>$(find -samefile channelcmd.template.cgi|sort)</pre>"



	elif [ -s /var/www/cgi-bin ];then
		CGI_BINDIR="/var/www/cgi-bin"
		echo "CGI_BINDIR = $(echo $CGI_BINDIR)"
		echo "going to CGI_BINDIR"
		cd $CGI_BINDIR
		echo "<br>"
		echo "finding old channels links, if any, that point to channelcmd.template.cgi and removing them"
		echo "<pre>find -samefile channelcmd.template.cgi</pre>"
		echo "<pre>$(find -samefile channelcmd.template.cgi -print|sort)</pre>"
		echo "<br>"
		echo "<pre>$(find .  -type f -name '[[:digit:]]*'.cgi -exec rm {} \;)</pre>"
		echo "<pre>$(find -samefile channelcmd.template.cgi -print|sort)</pre>"
		echo "Creating new links from channels.txt"
		echo "<pre>$(for i in $(cat /var/www/html/channels.txt);do ln -v channelcmd.template.cgi $i.cgi ; done)</pre>"
		echo "<br>"
		echo "Channel Links:"
		echo "<pre> </pre>"
		echo "<pre>$(find -samefile channelcmd.template.cgi|sort)</pre>"
	
	else 
		echo "no CGI-BIN directory found!"
		exit 1
	fi
else
	echo "No channels.txt in /var/www/html, exiting"
fi


echo "</body></html>"
