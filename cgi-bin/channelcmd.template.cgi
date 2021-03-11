#!/bin/bash
# License MIT

echo 'Content-type: text/html'
echo ""
echo "<html>"
echo "<head>"
echo "<title>Channel $CHANNEL</title>"
echo "<style>"
echo ".button {color:black;background-color:lime;font-size:72px;padding:1px 18%;border:2px solid black;text-decoration:none;border-radius:96px}"
echo ".button1 {color:black;background-color:red;font-size:36px;padding:1px 18%;border:2px solid black;text-decoration:none;border-radius:96px}"
echo "body {
  background-color: black;
  color: green;
}"
echo "h4 {text-align: center;}"
echo "p {text-align: center;}"
echo "p1 {text-align: right;}"

echo "div {text-align: center;}"
echo "div1 {text-align: right;}"
echo "</style>"
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<meta http-equiv='refresh' content='5;url=/index.html'>"
echo "<meta name="viewport" content="width=device-width, initial-scale=1.0">"
echo "</head>"
echo "<body>"



echo "<div>"
#prelaunch check
[[ "$(command -v bash)" ]] || { echo "bash is not installed" 1>&2 ; exit 1; }



[[ "$(command -v hls_stream_hdhr)" ]] || { echo "hls_stream_hdhr is not installed" 1>&2 ; exit 1; }

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
                echo "Unknown Linux"
		echo "<br>"
                echo "OS Test FAILED"
		echo "<br>"
		echo "CANT SET CGIBIN_DIR and APACHE_USER"
                exit 1  
        fi
else
        echo "Unknown OS"
        echo "OS Test FAILED"
        exit 1  
fi
echo "</div>"


echo "<div>"

. $(dirname "$0")/HDHR_IP.cgi #hdhr ip/hostname/fqdn referenced from external file
. $(dirname "$0")/HDHR_TUNER.cgi #hdhr tuner reference


#Check to make sure our ffmpeg copy(hls_stream_hdhr) for the primary stream  is NOT running as apache/httpd user process 
#the default below is a return value of 1, which means no matching process, proceeding to else
echo "<p>Testing cmd output(retval) from: pgrep hls_stream_hdhr -u $APACHE_USER >/dev/null</p>"
pgrep hls_stream_hdhr -u $APACHE_USER >/dev/null
retval=$?
if [ $retval -ne 1 ]; then
	echo "<h3><div class="w3-text-red">"
        echo "Return Value retval=$retval"
        echo "<h1>WARNING!</h1>"
        echo "<pre>1st STAGE 'hls_stream_hdhr' check! </pre>"
        echo "Primary stream process is  already running, ignoring new stream request."
	echo "</div>"
	echo "<h3><div class="w3-text-white">"
        echo "<h2><a href=/index.html>Return to index</a></h2>"
	echo "</div>"
        echo "</body></html>"
        exit 1
else
        echo "Our Test 'retval'=$retval "
	echo "Null reval=$retval, Passed Tests So Far. Proceeding."
	echo "</div>"
fi

echo "<p>$(echo $APACHE)</p>"

echo "</div>"


CHANNEL=0
##This assigns the script vars, based own its self/filename.
SNAME=$(basename "$0")
CHANNEL=$(echo $SNAME|cut -d. -f'1,2')
echo "<div>"
echo "SNAME PRECHECK=$SNAME"
echo "CHANNEL PRECHECK CHANNEL=$CHANNEL"
echo "</div>"

if [ $CHANNEL = 'channelcmd.template' ];then
	echo "<div>"
	echo "Uhh Ohhhh, channel is=$CHANNEL"
        echo "WARNING CHANNEL is $CHANNEL"
        echo "We don't have a channel yet, CHANNEL=$CHANNEL"
	echo "THIS SCRIPT DEPENDS ON CHANNEL DIRECTORIES NAMED $CHANNEL, yet $CHANNEL matches this filename, Not a Number such as '13.1'"
	echo "This likely means you have run this script direclty instead of the numbered channels scripts or you don't have CHANNEL DIRECTORIES SETUP YET IN ///hls/CHANNEL_NUMBER/"
        echo "Nothing to do, Exiting."
	echo "</div>"
        echo "</body></html>"
	exit 1
fi

if [ $CHANNEL = 0 ];then
	echo "<div>"
	echo "Uhh Ohhhh, channel is=$CHANNEL"
        echo "WARNING CHANNEL is $CHANNEL"
        echo "We don't have a channel yet, CHANNEL=$CHANNEL"
        echo "Nothing to do with a Channel0 Exiting."
	echo "</div>"
        echo "</body></html>"
	exit 1
fi


#sources external files for typical user easy configuration
. $(dirname "$0")/HTML_DIR.cgi #location of cgi-bin on OS
. $(dirname "$0")/HLS_SERVER.cgi #web/cgi server reference hostname/ip
. $(dirname "$0")/HDHR_PORT.cgi #hdhr port#DEFAULT 5004 referenced from external file
. $(dirname "$0")/HTTP_HLSDIR.cgi #ext http/hls dir reference
. $(dirname "$0")/FFOUTVCODEC.cgi #default FFmpeg video out codec reference



#VCODEC OPTS 
#
#todo:
#add more for hevc_nvenc h264_nvenc hevc_v4l2m2m h264_qsv hevc_qsv
#
#
#note: to use h264_omx or h264_v4l2m2m, either needs permissions on video
#usermod -aG video www-data or usermod -aG video apache #on redhat
#login/out your user and try again



if [ $FFOUTVCODEC == 'copy' ]; then
        FFOUTVCODEC='-c:v copy'
        #FFOUTVCODEC='-c:v copy -pix_fmt yuv420p'
elif [ $FFOUTVCODEC == 'h264_omx' ]; then
        FFOUTVCODEC='-c:v h264_omx -b:v 3M'
	#FFOUTVCODEC='h264_omx -b:v 20M -pix_fmt yuv420p -num_capture_buffers 32'
elif [ $FFOUTVCODEC == 'h264_v4l2m2m' ]; then
	#works somewhat
	FFOUTVCODEC='-c:v h264_v4l2m2m -pix_fmt yuv420p -b:v 6M'
	#FFOUTVCODEC='-c:v h264_v4l2m2m -num_capture_buffers 32 -pix_fmt yuv420p -b:v 8M'
elif [ $FFOUTVCODEC == 'libx264' ]; then
	#low compression hq settings
        #FFOUTVCODEC='libx264 -crf 18 -preset:v ultrafast -pix_fmt yuv420p' 
        #compatible
	# 8core option
	FFOUTVCODEC='-c:v libx264 -profile:v baseline -threads 8' 
else
	echo "Sorry Others Codec not configured yet"
	exit 1
fi

#future use
#mythtv server to pull schedule data from #note channel matching may not work with your mythtv setup
#. $(dirname "$0")/MYTHTV_SERVER.cgi #mythtv server


#internal references
HLSTARGETDIR=/var/www/html/hls/$CHANNEL
TARGETDIRTHUMBS=/var/www/html/thumbnails



#to make process management easier the primary stream is now hls_stream_hdhr
#which needs to be a copy of ffmpeg over to the $CGIBIN_DIR/
#done in seteup soon

HLS_STREAM_HDHR=$CGIBIN_DIR/hls_stream_hdhr
FFPROBE=/usr/bin/ffprobe
FFMPEGTHUMBNAILER=/usr/bin/ffmpegthumbnailer

##TODO_FEATURE: Have this try to pull the program duration from mythtv
#if not avail then fallback to a static time.
#HDHR_DURATION=$MYTHTV_DURATION|SCHEDULE DURATION|OTHERINPUTetc
HDHR_DURATION=3600

#the first video on the virtual channel should be on 0 on hdhr
#also reference other ways if not , such as by 0x31/Eng etc or 0:v
FFOUTVMAP="-map 0:0"

#Deinterlace content sd typically
#use this on a per channel basis until some sort of filter is added by resolution.
#could pull the width with ffprobe to make the choice
#FFOUTVFILTER='-vf yadif=0:-1:0,scale=trunc(iw/2)*2:trunc(ih/2)*2'

#the first audio on the virtual channel should be on 1 on hdhr
#also reference other ways if not , such as by 0x34/Eng etc or 0:a 
FFOUTAMAP="-map 0:1"

#I'm not sure of any reasons to change this with HLS unless your wanting to compile libfdk-aac and use it instead for higher quality sound.
FFOUTACODEC="-c:a aac -b:a 128k"


#read below about customized audio

########BUGZONE
#more recent version of ffmepg changes the channel layout default to 5.1(side)
#https://trac.ffmpeg.org/ticket/6974
#
#FFCHLAYOUT="-af channelmap=channel_layout=5.1"
#using the workaround provided above with channel_layout=5.1 only works well on HD channels
#sd channels with stereo only arent detected when this option is used


##########
#To use this need to add a ffprobe query to the channel before starting here and getting
#the streams LAYOUT/channeles then using that in our stream.
###################


#MINI HOWTO CUSTOMIZED AUDIO and/or VIDEO per CHANNEL
# per channel config is where you can define a specific command/processing
#per channel/stream. eg. if you want deinterlacing of sd channels, remove the channel
#link ##.#.cgi in question. Then copy this channelcmd.template file over to removed name.
#uncomment the Deinterlace option above #FFOUTVFILTER.
#Then only on that channel, your streams and mp4s will be deinterlaced.
#
#Could also individually configure a channel script too for any custom audio needed.
#EG.detailed
#all the channels are just hard links to --channelcmd.template.cgi
#just remove a channel link in question that you would like to customize.
#rm -rfv 28.4.cgi #for example.
#now copy channelcmd.template.cgi --> 28.4.cgi
#cp -av channelcmd.template.cgi 28.4.cgi
#now edit 28.4.cgi and change your audio channel configuration
#or many other optionss on a per-channel basis
#case in point prev, if your using all 5.1 channels by using channel-layout=5.1 in your main config.
#then you can use -ac 2 in your custom channel config.
#you could also map a different audio stream to be recorded instead of the default 0 map
#if your an audiophile maybe you want to hear classical on a different stream# and increase bitrate 
#you would use FFOUTAMAP=#STREAMYOUWNANT and increase the FFOUTACODEC value above.

#for now downmixing in this setup the following works for both without prefiltering stream audio types for now
#it works in vlc/mpv/mplayer/ffplay and with audio in audacious
FFOUTACH="-ac 2"


DASHPLAYLISTNAME=prog_index.mpd
FFHLSPLAYLISTNAME=playlist.m3u8
FFHLSSEGMENTNAME=out%04d.ts
FMP4FFHLSSEGMENTNAME=out%04d.m4s

FFHLSSEGTIME=6


#HTTP_HLSDIR=/hls
HTTP_HLSTARGETDIR=/hls/$CHANNEL
HTTP_TARGETDIRTHUMBS=/thumbnails
HTTP_HLS_STREAMING_URL=http://$HLS_SERVER/$HTTP_HLSTARGETDIR/$FFHLSPLAYLISTNAME


echo "<div>"
#
echo "<p>Checking tuner/channel for availability</p>"
#echo "<pre>$(echo ffprobe -f mpegts -i "http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL/?duration=1" 2>/dev/null)</pre>"
echo "<pre>$(ffprobe -f mpegts -i "http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=1" >/dev/null)</pre>"
FFPRETVAL=$?

if [ $FFPRETVAL -eq '1' ]; then
	echo "<h3><div class="w3-text-red">"
        echo "ERROR: FFPROBE RETURN VALUE REPORTED BACK NON-ZERO STATUS: FFPRETVAL=$FFPRETVAL"
        echo "</div>"
        echo "<div class="w3-text-yellow">"
        echo "HDHR TUNER=<b>http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL</b><i>reported BUSY, ignoring request.</i></h3>"
        echo "</div>"
        echo "<div class="w3-text-white">"
        echo "<pre><h3>Returning to index automatically</h3></pre>"
        echo "</div>"
        #this override is needed for refresh in this case to detect when a hdhr is busy.
        #when busy, without this check scripts will allow itself to proceed further down WRONGLY without error
        #the default above when tuner is available is to direct user to the stream creation  
        #the override pushes user back to index.html after the error notice
        echo "<head>"
        echo "<meta http-equiv='refresh' content='10;url=/index.html'>"
        echo "</head>"
        echo "</body></html>"
        exit 1
else
       	echo "<br>"
	echo "<div>"
        echo "HDHR Tuner Resource Ready. Processing Request, Standby for cleaning and prep..."
        echo "<br>"
        echo "</div>"
fi
echo "</div>"
sleep 2

echo "<div>"

#mpeg4 Management and recycling
FFCONCATMP4=playlist.mp4
FFCONCATMP4OLD=oldplaylist.mp4
FFCONCATMP4OLDER=olderplaylist.mp4
FFCONCATMP4OLDEST=oldestplaylist.mp4
FFCONCATMP4ELDEST=eldestplaylist.mp4

echo "<pre><i>Cleaning up & preparing directory for new stream on Ch $CHANNEL</i><br></pre>"
echo "<br>"
echo "<pre>$(rm -rf $HLSTARGETDIR/out*.ts $HLSTARGETDIR/playlist.m3u8)</pre>"


#echo $HLSTARGETDIR/$FFCONCATMP4 

#note script doesnt operate on eldestplaylist.mp4, it always gets overwritten first in the chain

if [ -s $HLSTARGETDIR/$FFCONCATMP4OLDEST ] ;then
        echo "oldestplaylist.mp4 exists. Moving to  eldestplaylist.mp4"
        echo "NOTE: eldestplaylist.mp4 will be overwritten with oldesplaylist."
        mv -v $HLSTARGETDIR/$FFCONCATMP4OLDEST $HLSTARGETDIR/$FFCONCATMP4ELDEST
elif [ -e $HLSTARGETDIR/$FFCONCATMP4OLDEST ] ;then
	#prob 0 byte file, lets not push that down the chain and overwrite old shows with 0 bytes!
	echo "removing 0 byte file"
	rm -fv $HLSTARGETDIR/$FFCONCATMP4OLDEST
fi

if [ -s $HLSTARGETDIR/$FFCONCATMP4OLDER ] ;then
        echo "olderplaylist.mp4 exists. Moving to  oldestplaylist.mp4"
        echo "NOTE: oldestplaylist.mp4 will be overwritten with olderplaylist."
        mv -v $HLSTARGETDIR/$FFCONCATMP4OLDER $HLSTARGETDIR/$FFCONCATMP4OLDEST
elif [ -e $HLSTARGETDIR/$FFCONCATMP4OLDER ] ;then
	#prob 0 byte file, lets not push that down the chain and overwrite old shows with 0 bytes!
	echo "removing 0 byte file"
	rm -fv $HLSTARGETDIR/$FFCONCATMP4OLDER 
fi


if [ -s $HLSTARGETDIR/$FFCONCATMP4OLD ] ;then
        echo "oldplaylist.mp4 exists. Moving to  olderplaylist.mp4"
        echo "NOTE: oldertplaylist.mp4 will be overwritten with oldplaylist."
        mv -v $HLSTARGETDIR/$FFCONCATMP4OLD $HLSTARGETDIR/$FFCONCATMP4OLDER
elif [ -e $HLSTARGETDIR/$FFCONCATMP4OLD ] ;then
	#prob 0 byte file, lets not push that down the chain and overwrite old shows with 0 bytes!
	echo "removing 0 byte file"
	rm -fv $HLSTARGETDIR/$FFCONCATMP4OLD
fi


if [ -s $HLSTARGETDIR/$FFCONCATMP4 ];then
        echo "playlist.mp4 exists. Moving to oldplaylist.mp4"
        mv -v $HLSTARGETDIR/$FFCONCATMP4 $HLSTARGETDIR/$FFCONCATMP4OLD
elif [ -e $HLSTARGETDIR/$FFCONCATMP4 ];then
	#prob 0 byte file, lets not push that down the chain and overwrite old shows with 0 bytes!
	echo "removing 0 byte file"
	rm -fv $HLSTARGETDIR/$FFCONCATMP4
fi


echo "<hr>"

echo "<h2>Starting Stream...</h2>"

echo "</div>"




#note we use setid here to fork off our jobs, when done on debian/redhat this means systemd will always be its
#PPID(1), we use this as identifier to monitor ffmpeg cmds in shell to prevent process crashes 



##start streaming

##for single file try adding
#-hls_flags single_file \
#and change FFHLSSEGMENTNAME to playlist.mp4
#then in ffmpegprocs.cgi disable the sections that start the conversion when idle


##option #1(BEST SO FAR).  hls type with event #tested with browswer plugin/vlc/mpv/ffplay, this works with hw hdhr transcoding
##note enabling the fragmented mpg4 option has audio sync problems, use mpegts containers for now
##-hls_flags program_date_time \
#
setsid $HLS_STREAM_HDHR -i "http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=$HDHR_DURATION" \
$FFOUTVMAP $FFOUTVCODEC \
$FFOUTAMAP $FFOUTACODEC \
$FFOUTACH \
-f hls \
-hls_segment_type mpegts \
-hls_time $FFHLSSEGTIME \
-hls_playlist_type event \
-master_pl_name $HLSTARGETDIR/$FFHLSPLAYLISTNAME \
-hls_base_url http://$HLS_SERVER$HTTP_HLSTARGETDIR/ \
-hls_segment_filename $HLSTARGETDIR/$FFHLSSEGMENTNAME \
$HLSTARGETDIR/$FFHLSPLAYLISTNAME \
&> /dev/null&


##option 2a dash/hls hybrid compatible type
##this is an interesting hybrid that produces both playlist.m3u8 and the dash prog_index.mpd
##the previews dont have links for the prog_index.mpd yet, so manually browese for now.
##note the hdhr transcode model still needs transcoded when using this since the hdhr transcode profiles are not
##fully compatible with this one
##i use libx264 with it

##when using hls opts ,need to be in the directory too or parse out some extra paths
#cd $HLSTARGETDIR

#setsid $HLS_STREAM_HDHR -i "http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=$HDHR_DURATION" \
#$FFOUTVMAP $FFOUTVCODEC \
#$FFOUTAMAP $FFOUTACODEC \
#$FFOUTACH \
#-f dash \
#-seg_duration $FFHLSSEGTIME \
#-dash_segment_type auto \
#-hls_playlist true \
#-hls_master_name $FFHLSPLAYLISTNAME \
#$DASHPLAYLISTNAME \
#&> /dev/null&


##option 2b dash compatible type
##this produces the dash prog_index.mpd #i tested with vlc
##the previews dont have links for the prog_index.mpd yet, so manually browese for now.
##note the hdhr transcode model still needs transcoded when using this since the hdhr transcode profiles are not
##fully compatible with this one
#setsid $HLS_STREAM_HDHR -i "http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=$HDHR_DURATION" \
#$FFOUTVMAP $FFOUTVCODEC \
#$FFOUTAMAP $FFOUTACODEC \
#$FFOUTACH \
#-f dash \
#-seg_duration $FFHLSSEGTIME \
#-dash_segment_type auto \
#$HLSTARGETDIR/$DASHPLAYLISTNAME \
#&> /dev/null&


##project original segment live,version. May have problems with vlc.
##note when using this option with +live, your system needs to be able to do realtime conversions
##option 1 segment type with LIVE
#setsid $HLS_STREAM_HDHR -i "http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=$HDHR_DURATION" \
#$FFOUTVMAP $FFOUTVCODEC \
#$FFOUTAMAP $FFOUTACODEC \
#$FFOUTACH \
#-f segment \
#-segment_format mpegts \
# -segment_list_type m3u8 \
#-segment_list $HLSTARGETDIR/$FFHLSPLAYLISTNAME \
#-segment_list_flags +live \
#-segment_time $FFHLSSEGTIME \
#$HLSTARGETDIR/$FFHLSSEGMENTNAME &> /dev/null&


echo "<div>"
echo "<pre>$(ps -C hls_stream_hdhr -o lstart)</pre>"
echo "<pre> Pid: $(ps -C hls_stream_hdhr -o pid=)</pre>"

echo "<hr>"
echo "<h2>Sleeping 10 seconds to allow stream time to  stabilize...</h2>"
sleep 10 
if [ -s "$HLSTARGETDIR/$FFHLSPLAYLISTNAME" ];then
	echo "<h1>Stream Stabilized and Ready!</h1>"
	echo "<a style=font-size:45px href=/index.html>Return to index</a>"
	echo "</div>"
	echo "</body></html>"
	exit 0
else
	echo "<h2><pre>Stream still not ready, sleeping 5 seconds more, then retrying....</pre></h2>"
	sleep 5
	if [ -s $HLSTARGETDIR/$FFHLSPLAYLISTNAME ];then
		echo "<h1>Stream Stabilized and Ready!</h1>"
		echo "<a style=font-size:45px href=/index.html>Return to index</a>"
		echo "</div>"
		echo "</body></html>"
		exit 0

	else
		echo "<h1>failure, could not detect playlist.m3u8</h1>"
		echo "<a style=font-size:45px href=/index.html>Return to index</a>"
		echo "><a href=/index.html>Return to index</a>"
		echo "</div>"
		echo "</body></html>"
		exit 1
	fi
fi
