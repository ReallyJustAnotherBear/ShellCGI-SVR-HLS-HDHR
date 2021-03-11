#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT

echo "Content-type: text/html"
echo ""
#echo "<html><head><title</title></head><body>"

#todo: sync this syntax up with channelcmd.template

#steps to get a web based installer going.
#have user test built in cgi
#have user enable cgi/d module and handler for .cgi

#have user install all *.cgi from git CGI-BIN dir and index to HTML dir
#have user start apache/httpd and then got to index.html

#using setup.cgi link at bottom of index.html
#if setup stage stamp complete disallow re-run unless removed marker.

#using form input from form at setup.cgi

#take variable input needed to get started such as HDHR_IP/CGIBIN_DIR
#default VCODEC, HDHR_IP, HDHR_PORT, HDHR_TUNER, HLS_SERVER, HTML_DIR

#GIVE USER CHECKBOX/SELECTION INPUTS for CODEC TYPE and ALL THESE LOCATIONS
