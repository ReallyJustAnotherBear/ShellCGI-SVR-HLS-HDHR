#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
set -o posix
echo 'Content-type: text/html'
echo ""
echo "<html>"
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<head>"
echo "<title>Create LiveTV Thumbnails</title>"
echo "<style>"
echo ".button1 {background-color: #4CAF50;}"
echo "body {
  background-color: black;
  color: green;
}"
echo "div {text-align: center;}"
echo "</style>"

echo "<meta http-equiv='refresh' content='5;url=/thumbnails.html'>"
echo "</head>"

echo "<body>"

echo "<br>"
echo "<br>"
echo "<br>"


echo "<div>"
. $(dirname "$0")/HDHR_IP.cgi
. $(dirname "$0")/HDHR_PORT.cgi
. $(dirname "$0")/HDHR_TUNER.cgi
. $(dirname "$0")/HLS_SERVER.cgi
. $(dirname "$0")/HLS_DIR.cgi
. $(dirname "$0")/HTML_DIR.cgi
. $(dirname "$0")/THUMBNAIL_DIR.cgi


FFMPEGTHUMBNAILER=/usr/bin/ffmpegthumbnailer

if [ ! -s $FFMPEGTHUMBNAILER ];then
	echo "<h4>Missing ffmpegthumbnailer, install first.</h4>"
	exit 1
fi

THUMBNAILSIZE=512 #0 is full size, 128 is default
#DATESTAMP ON THUMBS WHEN CREATED
TNDATE=`date +%Y%m%d-%H.%M%p`

echo "</div>"
#what host os?
#this sets up our CGIBIN_DIR and APACHE_USER
if [ $(uname) = 'Linux' ]; then
        #which apache or httpd?
        if [ -f /etc/debian_version ]; then
                echo "<div>"
                echo "Debian based OS"
                echo "<br>"
                echo "$(cat /etc/debian_version)"
                echo "<br>"
                echo "CGIBIN_DIR='/usr/lib/cgi-bin'"
                echo "<br>"
                echo "APACHE_USER='www-data'"
                CGIBIN_DIR='/usr/lib/cgi-bin'
                APACHE_USER='www-data'
                echo "OS Test Passed"
                echo "</div>"
        elif [ -f /etc/redhat-release ];then
                echo "<div>"
                echo "RedHat based OS"
                echo "<br>"
                echo "$(cat /etc/redhat-release)"
                echo "<br>"
                echo "CGIBIN_DIR='/var/www/cgi-bin'"
                echo "<br>" 
                echo "APACHE_USER='apache'"
                echo "<br>"
                CGIBIN_DIR='/var/www/cgi-bin'
                APACHE_USER='apache'
                echo "OS Test Passed"
                echo "</div>"
        else
                echo "<div>"
                echo "Unknown Linux"
                echo "<br>"
                echo "OS Test FAILED"
                echo "<br>"
                echo "CANT SET CGIBIN_DIR and APACHE_USER"
                echo "</div>"
		echo "</body></html>"
                exit 1
        fi
else

        echo "<div>"
        echo "Unknown OS"
	echo "<br>"
        echo "OS Test FAILED"
        echo "</div>"
	echo "</body></html>"
        exit 1
fi

#echo $APACHE_USER

        echo "<div>"
#precheck to make sure channels are avail
#this will be used in next section below after  a basic hls_stream_hdhr pretest
CHANNELSTXT=$HTML_DIR/channels.txt
CH1=$(head -n1 $CHANNELSTXT)
echo "<pre>$(cat $CHANNELSTXT|wc -l) channels</pre>"
echo "<pre>1st channel is $(echo $CH1) </pre>"
echo "<pre>Testing first channel: $CH1</pre>"
#timeout -k3 -s9 10 ffprobe http://$HDHR_IP:5004/$HDHR_TUNER/v$CH1 &>/dev/null
echo "<pre>$(/usr/bin/ffprobe -v error http://$HDHR_IP:5004/$HDHR_TUNER/v$CH1 &>/dev/null)</pre>"
FFPRETVAL=$?
	echo "</div>"

#First check to make sure hls_stream_hdhr is NOT running as apache/httpd user process spawned from PPID=1
#echo "pid of hls_stream_hdhr, if any:"
pgrep hls_stream_hdhr -u $APACHE_USER -P 1 &>/dev/null
retval=$?
if [ $retval -ne 1 ]; then
        echo "<div>"
    	echo "Return Value retval=$retval"
	echo "<h4>WARNING!</h4>"
	echo "<br>"
	echo "<h4>FFmpeg already running, ignoring new preview request.</h4>"
	echo "<br>"
	echo "<h4><a href=/index.html>Return to index</a></h4>"
	echo "</div>"
	echo "</body></html>"
	exit 1

elif [ $FFPRETVAL -ne '0' ];then
        echo "<div>"
	echo "No process clash detected but, our ffprobe returned NON ZERO status"
	echo "FFPROBE pre-test FFPRETVAL=$FFPRETVAL"
	echo "exiting with ERROR"
	echo "<br>"
	echo "<h4><a href=/index.html>Return to index</a></h4>"
	echo "</div>"
	echo "</body></html>"
	exit 1
else
        echo "<div>"
	echo "Passed FFMPEG pre-test retval=$retval"
	echo "Passed FFPROBE pre-test FFPRETVAL=$FFPRETVAL"
	echo "Processing Request, Standby..."
        echo "</div>"
fi
echo "<br>"

#clean stale targetdir png's each time we kick this off and make it this far.
if [ -d $THUMBNAIL_DIR ]; then
        echo "<div>"
	echo "Cleaning Stale Images from Targetdir."
	find $THUMBNAIL_DIR -name '[[:digit:]]*'.png -exec rm -rf $THUMBNAIL_DIR/*.png {} \; 
	echo "Cleaning done."
        echo "</div>"
else
        echo "<div>"
	mkdir -pv $THUMBNAIL_DIR
        echo "</div>"
fi
  
        echo "<div>"
#if not already exists, make our dir
[ -d $HLS_DIR ] || mkdir -pv $HLS_DIR
        echo "</div>"

cd $HLS_DIR

echo "<div>"
#terminate any stale procs we own
echo "Killing any stale ffmpegthumbnailer processes if any"
echo "<hr>"
echo "<br>"
killall -u $APACHE_USER ffmpegthumbnailer &>/dev/null

echo "<h4>Starting Preview Creation...Please wait...</h4>"
echo "<br>"
echo "</div>"


echo "<div>"
#echo "<pre>$(printf "\n")</pre>"

#autoassign channels to array from channel directories, 'digit filtered'
charray=($(for channeln in $(ls -dv *[[:digit:]].[[:digit:]]) ;do printf $channeln;printf '\n';done))
#calc n channels total
totalch=$(echo ${#charray[@]})

olrcount=0 #outer loop count
ilrcount=0 #inner loop count
olerrcount=0 #outer loop error count
ilerrcount=0 #inner loop error count
sumilerrcount=0 #sum of inner loop error resets. Each reset was 5 tries.
channeln=0 # this is our iterate channel number

#loop through channel array 
for channeln in ${charray[@]};do
	#mark the olrcount on every iteration from 0+ for the outside loop, this matches n channels avail and 
	#indexes every channel into the loop starting from 0, associated with lowest channel number(*major.minor)
	#this is our main identifier for each channel as it passes through from 0-nCh
	((olrcount++))
	sleep .10
        echo "<h4>Processing Request for Channel=$channeln, Standby...</h4>"
	echo " "
	while [ $olrcount -lt $totalch ]|[ $olerrcount -lt $totalch ];do
		#mark the ilrcount(inside loop run count) on every iteration from 0+, the starts cmd processing 
		#per channel and loops up to the channels available, retrying up to the # channels avail.
		((ilrcount++))
		
		##FFMPEG METHOD WITH WRITE ON IMAGE INLINE, 6 seconds for each preview gen
		#/usr/bin/ffmpeg -i http://192.168.168.2:5004/tuner1/v13.1 -ss 00:00:00 \
		#-vframes 1 -vf drawtext=text="'$CH-$DATE':fontcolor=white:fontsize=75:x=100:y=100,scale=512:-1" \
		#/var/www/html/thumbnails/13.1.png

		#if thumbnailer hangs or doesn't finish each preview in less than 8+6, kill with signal -9
		time timeout -k6 -s9 8 /usr/bin/ffmpegthumbnailer -f -i http://"$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$channeln" \
		-t0 -s$THUMBNAILSIZE \
		-o $THUMBNAIL_DIR/$channeln.png
		retvalcn=$?
		if [ $retvalcn == '0' ]; then
			echo "<h4><div class="w3-text-lime"</h4>"
        		echo "outer loop run count=$olrcount"
        		echo "outer loop error count=$olerrcount"
        		echo "inner loop run count=$ilrcount"
        		echo "inner loop error count=$ilerrcount"
			echo "Current Sum of ilerrcount resets=$sumilerrcount"
			echo "<br>"
			echo "<br>"
        		echo "Channeln Return Value retvalcn=$retvalcn"
			echo "<div class="w3-text-white">"
			echo "<h4><i>"Channel Preview Image for $channeln.png Completed."</i></h4>"
			echo "<br>"
			echo "<br>"
			echo "</div>"
			echo "</div>"
			break
		elif [ $retvalcn -eq 1 ]; then
			((ilerrcount++))
			echo "<h4><div class="w3-text-red"</h4>"
        		echo "outer loop run count=$olrcount"
        		echo "outer loop error count=$olerrcount"
        		echo "inner loop run count=$ilrcount"
        		echo "inner loop error count=$ilerrcount"
			echo "Current Sum of ilerrcount resets=$sumilerrcount"
			echo "<br>"
	        	echo "<h4>WARNING! virtual Channel Missing or error 404</h4>"
			echo "<h4>FfmpegThumbnailer Return Value=$retvalcn, is not=0 </h4>"
			echo "<h4>Failed new preview request for $channeln on TestTry#:$olrcount</h4>"
			echo "<br>"
        		echo "<h4>HDHR TUNER=http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$channeln </h4>"
        		echo "</div>"
			continue

		elif [ $retvalcn -eq 137 ]; then
			((ilerrcount++))
			echo "<h4><div class="w3-text-red"</h4>"
        		echo "outer loop run count=$olrcount"
        		echo "outer loop error count=$olerrcount"
        		echo "inner loop run count=$ilrcount"
        		echo "inner loop error count=$ilerrcount"
			echo "Current Sum of ilerrcount resets=$sumilerrcount"
			echo "<br>"
	        	echo "<h4>WARNING! virtual Channel TimedOut with errors </h4>"
			echo "<h4>FfmpegThumbnailer Return Value=$retvalcn, is not=0 </h4>"
			echo "<h4>Failed new preview request for $channeln on TestTry#:$olrcount</h4>"
			echo "<br>"
        		echo "</div>"
			continue

		elif [ $retvalcn -eq 255 ]; then
			((ilerrcount++))
			echo "<h4><div class="w3-text-red"</h4>"
        		echo "outer loop run count=$olrcount"
        		echo "outer loop error count=$olerrcount"
        		echo "inner loop run count=$ilrcount"
        		echo "inner loop error count=$ilerrcount"
			echo "Current Sum of ilerrcount resets=$sumilerrcount"
			echo "<br>"
	       		echo "<h4>WARNING! Channel Unavail or Busy with ERROR 503 </h4>"
			echo "<h4>FfmpegThumbnailer Return Value=$retvalcn, is not=0 </h4>"
			echo "<h4>Failed new preview request for $channeln on TestTry#:$olrcount</h4>"
			if [ $ilerrcount -gt '2' ];then
				echo "<br>"
				echo "<h4><div class="w3-text-orange"</h4>"
        			echo "<h4>ERROR:Preview Generation for $channeln has failed $ilerrcount times.</h4>"
        			echo "<h4>echo removing  ERRORED $channeln array reference</h4>"
				#not unset sets the ref to null but keep indexes without reordering
				#watch out for trailing spaces that may need to be trimmed 
				#echo "<pre>$(unset charray[$channeln])</pre>"
				#echo ${charray[@]/$channeln}
				echo "<pre>$(echo charray[@]/$channeln])</pre>"
				echo "reseting inner loop error count to zero after removal of array reference"
				echo "<pre>$(echo ${charray[@]})</pre>"
				echo "tracking total ilerrcount with sumilerrcount"
				((sumilerrcount++))
				ilerrcount=0
				echo "Current Sum of ilerrcount resets=$sumilerrcount"
        			echo "</div>"
				break
			else	
				echo "<br>"
				echo "<h4><div class="w3-text-yellow"</h4>"
        			echo "<h4>This Channel $channeln will be tested again</h4>"
		   	        echo "<h4>this is try #: $ilerrcount of outer loop run# $olrcount, and inner loop run# $ilrcount</h4>"
				echo "<br>"
        			echo "</div>"
				continue
			fi
        		echo "</div>"
			continue
		else
			((olerrcount++))
			echo "<h4>FfmpegThumbnailer Return Value=$retvalcn, is not=0 </h4>"
			echo "<div class="w3-text-red">"
        		echo "outer loop run count=$olrcount"
        		echo "outer loop error count=$olerrcount"
        		echo "inner loop run count=$ilrcount"
        		echo "inner loop error count=$ilerrcount"
			echo "Current Sum of ilerrcount resets=$sumilerrcount"
			echo "<br>"
			echo "<h4>ERROR UNDEFINED CONDTION</h4>"
			#todo add another level of filter here to catch at least one or two more conditions. 127/??
#        		echo "<pre>Returning to index automatically </pre>"
#        		echo "</div>"
#			#the override pushes user back to index.html
#			echo "<head>"
#			echo "<meta http-equiv='refresh' content='4;url=/index.html'>"
#			echo "</head>"
        		echo "</div>"
#      	       		echo "</body></html>"
#       		exit 1
 			#continue	
			break
		fi
	done
done
echo "</div>"
echo "<pre>$(unset 'channeln')</pre>"
echo "<hr>"
echo "<br>"

echo "<h4><div class="w3-text-yellow">"
echo "Preview Image generation  Done!"
echo "</div></h4>"
echo "<br>"


echo "<div>"
#DYNAMIC HTML START
#This opens and writes the initial templated html out to >> /thumbnails.html           #soon to be /previews.html
echo '<html>
 <head>
  <title>LiveTV Last Previews</title>
  <link rel="stylesheet" type="text/css" href="/w3.css">
  <meta http-equiv="pragma" content="no-cache" />
  <meta http-equiv="refresh" content="300;URL=/index.html">
  <style>body {
  	background-color: black;
  	color: green;
	}	
  </style></head><body>'>$HTML_DIR/thumbnails.html
echo "</div>"

#This writes(appends) out our header that has our bar at top
echo "<div>"
echo '<header>
 <div class="w3-top">
  <div class="w3-bar w3-dark-grey w3-card-4 ">
   <a href="/index.html" class="w3-bar-item w3-button w3-mobile w3-xxlarge">Home</a>
   <div class="w3-dropdown-hover">
   <button class="w3-button w3-xxlarge">LiveTV</button>
   <div class="w3-dropdown-content w3-bar-block w3-card-4">
    <a href="/thumbnails.html" class="w3-bar-item w3-button w3-mobile w3-xxlarge">Direct Stream from Channel Previews</a>
    <a href="/cgi-bin/createthumbnails.cgi" class="w3-bar-item w3-button w3-mobile w3-xxlarge">Update All Channels Previews. Then Select Channel to Stream</a>
  </div>
  </div>
  <div class="w3-dropdown-hover">
  <button class="w3-button w3-xxlarge">mp4 Videos</button>
   <div class="w3-dropdown-content w3-bar-block w3-card-4">
    <a href="/prevstreamed_thumbnails.html" class="w3-bar-item w3-button w3-mobile w3-xxlarge">Select/Play Directly from Video Previews</a>
    <a href="/cgi-bin/createthumbnails_prevstreamed.cgi" class="w3-bar-item w3-button w3-mobile w3-xxlarge">Scan4New/Update Video Previews before Selection</a>
  </div>
  </div>
  <div class="w3-dropdown-hover">
  <button class="w3-button w3-xxlarge">HDHomeRun</button>
   <div class="w3-dropdown-content w3-bar-block w3-card-4">
    <a target="_blank" rel="noopener noreferrer" href="http://HDHR-01234567" class="w3-bar-item w3-button w3-mobile w3-xxlarge">Web Device Home Page</a>
    <a href="http://192.168.1.218/lineup_status.json" class="w3-bar-item w3-button w3-mobile w3-xxlarge">HDHR-LineupStatus</a>
    <a target="_blank" rel="noopener noreferrer" href="http://HDHR-01234567/lineup.post?scan=start" class="w3-bard-item w3-button w3-mobile w3-xxlarge">HDHR-ScanChannels</a>
  </div>
  </div>
  <div class="w3-dropdown-hover">
  <button class="w3-button w3-xxlarge">MythTV</button>
   <div class="w3-dropdown-content w3-bar-block w3-card-4">
    <a href="#" class="w3-bar-item w3-button"></a>
    <a target="_blank" rel="noopener noreferrer" href="http://MYTHTVSERVER.LOCALDOMAIN:6544" class="w3-bar-item w3-button w3-mobile w3-xxlarge">MythTV-Server</a>
    <a target="_blank" rel="noopener noreferrer" href="http://MYTHTVSERVER.LOCALDOMAIN:6544/tv/guide.qsp"class="w3-bar-item w3-button w3-mobile w3-xxlarge">MythTV-ProgramGuide</a>
   </div>
  </div>
 </div>
</header>'>>$HTML_DIR/thumbnails.html
echo "</div>"


  
echo "<div>"
#This finds channel numbers from directory names in HLS and loops through them and creates the links
#for the html to start the streams, then writes(appends) it out to >> /thumbnails.html #soon to be /previews.html
channeln=0
#
#the ls -v sorts the channels by itself
echo "<pre>"
channelnruncount=0
for channeln in $(ls -dv *[[:digit:]].[[:digit:]] 2>/dev/null);do
	((channelnruncount++))
echo "channelnruncount=$channelnruncount"
echo '<br>
<br>
<br>
<br>
<div style="text-align:center">
 <a href="http://'$HLS_SERVER'/cgi-bin/'$channeln'.cgi" class="button1"><img src="/thumbnails/'$channeln'.png" alt="'$channeln'.png"><!--- COMPAT --></a>
 <h4>'ch$channeln-$TNDATE'</h4>
 <hr><br>
</div>
<br>'>>$HTML_DIR/thumbnails.html
done
echo "Dynamic Html: Link generation of $channelnruncount Channels Done!"
echo "</pre>"
unset 'channeln'
echo "</div>"


echo "<div>"
#This writes out and finalizes the /thumbnail.html page.
echo "</body></html>">>$HTML_DIR/thumbnails.html
#DYNAMIC HTML END
echo "</div>"

echo "<hr>"
#The following html closes this page out.
echo "</body></html>"
#createthumbnails.cgi 
