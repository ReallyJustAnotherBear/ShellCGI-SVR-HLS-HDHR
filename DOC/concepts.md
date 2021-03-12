

The idea is you can use a linux/unix/windows box to transcode a media source from a web page click, which in return creates the HLS files and .m3u8 resource file.

I happen to use a silicon dust hdhr-extend which has hw transcode for my input. This works well because all that is needed for a compatible HLS stream is a re-encode of the audio to aac. You could re-encode completely with libx264/ffmpeg without a hw encoder as well, you just have to change the channel script stanzas.

Eg.
If your hdhr is setup on your local network you should be able to directly stream from it with a line simiilar to:
```URL LAYOUT for HDHR
http://HDHR_IP:PORT:TUNERID/CHANNEL
```

Playback example:
```
ffplay http://HDHR_IP:5004/tuner1/v13.1
```  
 or vlc,mplayer, etc
    *In this example my channel is "v13.1". Note by default you might be streaming raw mpeg-2 TS or with a hdhr-extend you might be using a h264 profile                by default. This standard stream is not ready for HLS/iphones or any. It likely only will work with players like ffplay/vlc/mplayer. To get this into a format your idevice or other HLS client can use. You need to have the video in h264 and the audio in aac format.

Here's the same RESOURCE ,but now it is HLS ready, thanks to ffmpeg

*Note this version is using hw encoding due to to conversion of the video codec
```
ffmpeg -i http://HDHR_IP:5004/tuner1/v13.1 -codec:a aac -f ssegment -segment_list playlist.m3u8 -segment_list_flags +live -segment_time 10 out%03d.ts
```

*Then, note this version is using all SW encoding
```
ffmpeg -i http://HDHR_IP:5004/tuner1/v13.1 -vcodec libx264 -codec:a aac -f ssegment -segment_list playlist.m3u8 -segment_list_flags +live -segment_time 10 out%03d.ts
```
*In the above stanza's you can see that a playlist.m3u8 is going to be generated in the current directory when this is run as is the output of *.ts files. For example now I will modify the stanza to point to my /var/www/html/hls/13.1 directory location.
```
ffmpeg -i http://HDHR_IP:5004/tuner1/v13.1 -vcodec libx264 -codec:a aac -f ssegment -segment_list /var/www/html/hls/13.1/playlist.m3u8 -segment_list_flags +live -segment_time 10 /var/www/html/hls/13.1/out%03d.ts
```

Once these files are output to your destination, they may need chmod'd  to 0755, if you don't have "g+s" set on your output directory. 
I chown'd my scripts to run under the same account as the web server runs under, but you can reconfigure as needed for you home setup.



Not just apache, but just about webserver with cgi enabled could work.

After the source, Ffmpeg does all the work for conversion and HLS segmenting.
The webserver then does the work of hosting the files to clients and starting and stopping the streams via cgi-bin web scripts.

This is very rudimentary but effective and simple once setup to use.

***Todo(s):***
***killall script should be changed to match by PID of running, buttons should indicate which is pressed currently(in use), process shouldnt keep locked on browser once submitted, it needs released(but currently still processes), output needs tagged better with datetime stamp, needs a cleanup routine***

#### Tips for modifying for use with other inputs besides hdhr.
To use this with a dvb device, you will need to create a channel list/scan for channels with dvbv5-zap, then call the channel up like so:
```
#dvbv5-zap -c channels.conf -r '13.1'
```
Once dvbv5-zap is  channel locked, then ffmpeg can do it's magic with using input directly from:
```
 /dev/dvb/adapter0/dvr0
```
Remember ffmpeg can't grab it until the channel/multiplex is locked, so it will need to be called just prior to ffmpeg processing attempts on /dev/dvb/adapter*/dvr*

You might try adding something like $((/path/to/dvbv5-zap -c /path/to/channels.conf -r '13.1'),(ffmpeg -i /dev/dvb/adapter***)) or similar to your new stanza.
