#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#createthumbnails_prevstreamed.cgi
set -o posix
printf "Content-type: text/html\n\n"
echo "<html>"
echo "<head>"
echo "<title>PrevStreamed</title>"
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<style>"
echo ".button1 {background-color: #4CAF50;}"
echo "body {
  background-color: black;
  color: green;
}"
echo "h3 {text-align: left;}"
echo "h4 {text-align: center;}"
echo "p {text-align: center;}"
echo "p1 {text-align: left;}"
echo "div {text-align: center;}"
echo "</style>"
echo "<meta http-equiv='refresh' content='3;url=/prevstreamed_thumbnails.html'>"
echo "</head>"
echo "<body>"

echo "<br>"
echo "<br>"
echo "<br>"


. $(dirname "$0")/HDHR_IP.cgi
. $(dirname "$0")/HDHR_PORT.cgi
. $(dirname "$0")/HDHR_TUNER.cgi
. $(dirname "$0")/HLS_SERVER.cgi
. $(dirname "$0")/HLS_DIR.cgi
. $(dirname "$0")/HTML_DIR.cgi
. $(dirname "$0")/PREVSTREAMED_THUMBNAIL_DIR.cgi

FFMPEGTHUMBNAILER=/usr/bin/ffmpegthumbnailer
#CHANNELS.TXT=$HTML_DIR/channels.txt
THUMBNAILSIZE=512 #0 is full size, 128 is default
TIMESEEKIN=7

DURATION='ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 -sexagesimal'



#if not already exists, make our dir
[ -d $HLS_DIR ] || mkdir -pv $HLS_DIR

#cd $HLS_DIR

echo "<hr>"
echo "<div>"
echo "<h2>Generating images...Please wait</h2>"
#thumbnail references to previous HLS streams Converted to mpeg4's,  these .pngs generated from the *playlist.mp4 files
echo "</div>"

echo "<div>"


#NEXT NARROWER TEST include find
#find /var/www/html/hls/*/ -type f -iname "*playlist.mp4" \
#-not -empty -printf '%p      \t' -exec bash -c \
#'ffmpegthumbnailer -w -f -i $channelTaggedPlaylistMp4 -t $TIMESEEKIN -s$THUMBNAILSIZE -o $channelTaggedPlaylistMp4.png' {} \;
#'/usr/bin/ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 -sexagesimal $0' {} \;

mp4pngscount=0
for channelTaggedPlaylistMp4 in $(ls -dv /var/www/html/hls/*[[:digit:]].[[:digit:]]/*playlist.mp4 2>/dev/null);do
	(( mp4pngscount++ ))
	ffmpegthumbnailer -w -f -i $channelTaggedPlaylistMp4 -t $TIMESEEKIN -s$THUMBNAILSIZE -o $channelTaggedPlaylistMp4.png
        echo "<br>"
        echo "<div class="w3-text-white">"
        echo "<h2>" Mpeg4 Video $channelTaggedPlaylistMp4.png Preview Image $mp4pngscount 100% Done."</h2>"
        echo "<br>"
        echo "<br>"
        echo "</div>"
done

echo "<pre>$(unset 'channelTaggedPlaylistMp4')</pre>"
echo "<hr>"
echo "<br>"
echo "<h2>"
echo "<div class="w3-text-yellow">"
echo "Video Preview Image generation of $mp4pngscount mpeg4s Done!"
echo "</div</h2>"

echo "</div>"
echo "<br>"

#DYNAMIC HTML START
#This opens and writes the initial templated html out to >> /prevstreamed_thumbnails.html           #soon to be /previews.html
echo '<html>
 <head>
  <title>mp4 Video Previews</title>
  <link rel="stylesheet" type="text/css" href="/w3.css">
  <meta http-equiv="Cache-Control" content="no-cache" />
  <meta http-equiv="pragma" content="no-cache" />
  <meta http-equiv="refresh" content="300;URL=/index.html">
  <style>body {
        background-color: black;
        color: green;
        }       
  </style></head><body>'>$HTML_DIR/prevstreamed_thumbnails.html

#This writes(appends) out our header that has our bar at top >>/prevstreamed_thumbnails.html
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
</header>'>>$HTML_DIR/prevstreamed_thumbnails.html



echo "<div>"
#cd $HLS_DIR

#This adds links from the mpeg4's converted from hls to the previouslystreamed_thumbnails.html page
echo "<pre>"
mp4linkscount=0
for i in $(ls -dv /var/www/html/hls/*[[:digit:]].[[:digit:]]/*playlist.mp4 2>/dev/null);do
(( mp4linkscount++ ))
SIZE=$(du -sh $i)
CHPATH=${i#*hls/}
FILENAMEEXT=${i##*/}
CHANNEL=${CHPATH%/*playlist.mp4}
echo '<br>
<br>
<br>
<br>
<div style="text-align:center">
<a href="http://'$HLS_SERVER'/hls/'$CHPATH'" class="button"><img src="/hls/'$CHPATH'.png" alt="/hls/'$CHPATH'.png"><!--- COMPAT --></a>
<h1>'$(echo Channel $CHANNEL)'</h1>
<h1>'$(echo $FILENAMEEXT)'</h1>
<h1>'$(echo $($DURATION -i $i|cut -d. -f1))'</h1>
<h1>'$(du -sh $i)'</h1>
<hr>
<br>
</div>
<br>'>>$HTML_DIR/prevstreamed_thumbnails.html
done
echo "link generation for $mp4linkscount mpeg4s Done!"
echo "</pre>"


#This adds footer, writes out and finalizes the /prevstreamed_thumbnails.html page.
echo "</body></html>">>$HTML_DIR/prevstreamed_thumbnails.html
#DYNAMIC HTML END

echo "<hr>"
#This html closes this page, createthumbnails_prevstreamed.cgi.
echo "</div>"   
echo "</body></html>"

#createthumbnails_prevstreamed.cgi
