#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#set -x
CHANNELS=/var/www/html/channels.txt
if [ -s $CHANNELS ];then
	echo "You already have Channels:"
	cat $CHANNELS
	echo "Backing up old $CHANNELS to $CHANNELS.OLD"
	cp -v $CHANNELS $CHANNELS.OLD
	#check cgi-bin dir location and set
	if [ -d /usr/lib/cgi-bin ];then 
		CGI_BINDIR="/usr/lib/cgi-bin"
		echo "CGI_BINDIR = $(echo $CGI_BINDIR)"
		echo "going to CGI_BINDIR"
		cd $CGI_BINDIR
		echo " "
		echo "finding old channels links, if any, that point to channelcmd.template.cgi and removing them"
		find -samefile channelcmd.template.cgi -print|sort
		echo " "
		find .  -type f -name '[[:digit:]]*'.cgi -exec rm {} \;
		find -samefile channelcmd.template.cgi -print|sort
		echo "Creating new links from channels.txt"
		for i in $(cat /var/www/html/channels.txt);do ln -v channelcmd.template.cgi $i.cgi ; done
		echo " "
		echo "Channel Links:"
		find -samefile channelcmd.template.cgi|sort



	elif [ -d /var/www/cgi-bin ];then
		CGI_BINDIR="/var/www/cgi-bin"
		echo "CGI_BINDIR = $(echo $CGI_BINDIR)"
		echo "going to CGI_BINDIR"
		cd $CGI_BINDIR
		echo " "
		echo "finding old channels links, if any, that point to channelcmd.template.cgi and removing them"
		find -samefile channelcmd.template.cgi -print|sort
		echo " "
		find .  -type f -name '[[:digit:]]*'.cgi -exec rm {} \;
		find -samefile channelcmd.template.cgi -print|sort
		echo "Creating new links from channels.txt"
		for i in $(cat /var/www/html/channels.txt);do ln -v channelcmd.template.cgi $i.cgi ; done
		echo " "
		echo "Channel Links:"
		find -samefile channelcmd.template.cgi|sort
	
	else 
		echo "no CGI-BIN directory found!"
		exit 1
	fi
else
	echo "No channels.txt in /var/www/html, exiting"
fi
