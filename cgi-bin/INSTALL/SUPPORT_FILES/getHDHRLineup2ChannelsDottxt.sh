#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
. $(dirname "$0")/HDHR_IP.cgi #hdhr ip/hostname/fqdn referenced from external file
. $(dirname "$0")/HDHR_HTTPPORT.cgi #hdhr http port

echo $HDHR_IP 
echo $HDHR_HTTPPORT



curl  -s http://$HDHR_IP:$HDHR_HTTPPORT/lineup.xml|xmlstarlet sel -T -t -v "//GuideNumber" -n > /var/www/html/channels.txt

#getHDHRLineup2ChannelsDottxt.sh
