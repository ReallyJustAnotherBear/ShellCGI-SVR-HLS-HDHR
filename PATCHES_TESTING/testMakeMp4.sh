#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
echo "Content-type: text/html"
echo ""
echo "<html>"
echo "<head>"
echo "</head>"
echo "<title></title></head>"
echo ""
echo "<style>"
echo ".button0 {color:black;background-color:red;width:50%;font-size:32px;padding:4px 2px;border-radius:24px;text-decoration:none}"
echo ".button {color:black;background-color:lime;font-size:72px;padding:1px 18%;border:2px solid black;text-decoration:none;border-radius:96px}"
echo "</style>"

echo "<body>"

CHANNEL=13.3

FFMPEG="/usr/bin/ffmpeg"
HDHR_IP=192.168.4.7
HDHR_PORT=5004
HDHR_TUNER=auto
HDHR_DURATION=33 #seconds
#FFOUTVCODEC=copy
##RPI4 try/also try omx below on rpi4 as well
#FFOUTVCODEC="h264_v4l2m2m -b:v 8M"
FFOUTVCODEC="h264_omx -b:v 8M"
FFOUTACODEC=aac
FFOUTAMAP=0
FFOUTACH="-ac 2"
HLSTARGETDIR=/var/www/html/hls/$CHANNEL
FFHLSPLAYLISTNAME=playlist.m3u8
FFHLSSEGMENTNAME=out%04d.ts
FFHLSSEGTIME=10

FFCONCATMP4=playlist.mp4
FFCONCATMP4OLD=oldplaylist.mp4
FFCONCATMP4OLDEST=oldestplaylist.mp4

#echo $HLSTARGETDIR/$FFCONCATMP4 

if [ -f $HLSTARGETDIR/$FFCONCATMP4OLD ] ;then
	echo "oldplaylist.mp4 exists. Moving to  oldestplaylist.mp4"
	mv -v $HLSTARGETDIR/$FFCONCATMP4OLD $HLSTARGETDIR/$FFCONCATMP4OLDEST
fi

if [ -f $HLSTARGETDIR/$FFCONCATMP4 ];then
	echo "playlist.mp4 exists. Moving to oldplaylist.mp4"
	mv -v $HLSTARGETDIR/$FFCONCATMP4 $HLSTARGETDIR/$FFCONCATMP4OLD
fi

rm -rfv $HLSTARGETDIR/$FFHLSPLAYLISTNAME $HLSTARGETDIR/out*.ts


echo "URL is http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=$HDHR_DURATION"

echo "<pre>$DAEMON $($FFMPEG -i http://$HDHR_IP:$HDHR_PORT/$HDHR_TUNER/v$CHANNEL?duration=$HDHR_DURATION -c:v $FFOUTVCODEC -c:a $FFOUTACODEC -map $FFOUTAMAP $FFOUTACH -f segment -segment_list $HLSTARGETDIR/$FFHLSPLAYLISTNAME -segment_list_flags +live -segment_time $FFHLSSEGTIME $HLSTARGETDIR/$FFHLSSEGMENTNAME ; $FFMPEG -f concat -safe 0 -i <(for f in $HLSTARGETDIR/*.ts; do echo "file '$f'"; done) -c copy $HLSTARGETDIR/playlist.mp4)</pre>"

echo "</body></html>"
