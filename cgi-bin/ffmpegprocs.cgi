#!/bin/bash
# (c) 2021-03-10
# License MIT
#ffmpegprocs.cgi
set -o posix
. $(dirname "$0")/HDHR_IP.cgi
. $(dirname "$0")/HLS_SERVER.cgi
. $(dirname "$0")/HTTP_HLSDIR.cgi
echo "Content-type: text/html"
echo ""
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<html>"
echo "<head>"
echo "<title>ffmpeg/hls_stream_hdhr running procs</title>"
#careful. This can force refreshs and cause checks for new hls segments>mp4 that could compete with user intentions/interactions.
echo '<meta http-equiv="refresh" CONTENT="60">'
echo "<style>"
echo ".button0 {color:black;background-color:red;width:50%;font-size:32px;padding:4px 2px;border-radius:24px;text-decoration:none}"
echo ".button {color:black;background-color:lime;font-size:64px;padding:1px 18%;border:2px solid black;text-decoration:none;border-radius:96px}"
echo "body {
  background-color: black;
  color: green;
}"
echo "h4 {text-align: center;}"
echo "p {text-align: center;}"
echo "div {text-align: center;}"
echo "</style></head>"
echo "<body>"
echo "<header>"
echo "</header>"
echo "<br>"
echo "<br>"

echo "<div>"
#what host os?
#this sets up our CGIBIN_DIR and APACHE_USER
if [ $(uname) = 'Linux' ]; then
        printf "<br>"
        printf "<br>"
        if [ -f /etc/debian_version ]; then
		echo "Debian based OS"
                echo "<br>"
	       	echo "v$(cat /etc/debian_version)-$(lsb_release -sc)"
                CGIBIN_DIR='/usr/lib/cgi-bin'
                APACHE_USER='www-data'
        elif [ -f /etc/redhat-release ];then
                echo "RedHat based OS"
                echo "<br>"
		echo "$(cat /etc/redhat-release)"
                echo "<br>"
                CGIBIN_DIR='/var/www/cgi-bin'
                APACHE_USER='apache'
        else
                echo "Undefined Linux"
                echo "OS Test FAILED"
                echo "CANT SET CGIBIN_DIR and APACHE_USER"
                echo "</div>"
                echo "</body></html>"
                exit 1
        fi
else
        echo "Unknown OS"
        echo "OS Test FAILED"
        echo "</div>"
        echo "</body></html>"
        exit 1
fi
echo "<div class="w3-text-light-green">"
echo "<pre>Using HDHR Device at: $HDHR_IP</pre>"
TUNER1VCTSTATUS=$(curl -s hdhomerun.local/status.json | jq -r '.[1].VctNumber')
TUNER1IPSTATUS=$(curl -s hdhomerun.local/status.json | jq -r '.[1].TargetIP')
if [ $TUNER1VCTSTATUS != 'null' ];then
	echo "Device busy/resource locked with Channel=$TUNER1VCTSTATUS for Host with IP=$TUNER1IPSTATUS"
fi
echo "</div>"
#even though we use a specific primary stream binary now of ffmpeg (hls_stream_hdhr). 
#We still use ffmpeg as well for now for the m3u8>mp4 conversions.
#may switch to a conversion process name for it in future as well to make process management even more simple and potentially more portable.
FFMPEG=/usr/bin/ffmpeg

#streaming channel
SCHANNEL=0


#track counts errors on conversions 
conv_errcount=0

#our 'hls_stream_hdhr' specific process for primary stream recognition should be in the $CGIBIN_DIR/
#primary streaming process detection
(pgrep -x hls_stream_hdhr -u $APACHE_USER &>/dev/null)
retval=$?
#here we must decide if we want to show channel buttons to view/stop streams or convert hls segments to mp4's.
#if our retval above evaulates to 0(true), then the primary stream process is assumed to be running and we skip down to the else
#section where we show our start/stop buttonse
#Else we start here if we get a retval of 1 back.

#func to check/show ffmpeg ps stats
pgrepffmpeg_func() {
	#here we are looking for conversion processes not primary stream processes
	(pgrep -x ffmpeg -u $APACHE_USER &>/dev/null)
	retvalffmpeg=$?
	if [ $retvalffmpeg -eq 0 ];then
		echo "<div class="w3-text-white">"
        	echo "<div style="text-align:left">"
        	echo "<pre><small><i>$(ps -C ffmpeg -o lstart,user,pid,ppid,%cpu,%mem,cmd --width 500)</i></small></pre>"
        	echo "</div>"
        	echo "</div>"
	fi	
}



#with a return(retval) of '1', (or FALSE, that primary process detected running), we run the conversions here in this section.
if [ $retval -eq 1 ]; then
	echo "<h4>"
	echo "<div class="w3-text-yellow">"
	echo "<pre><small><i><p>Streaming not detected, not showing 'stop/watch' buttons for stream control.</p></i></small></pre>"
	echo "<pre><small><i>During FFmpeg idle/page refresh, HLS segments are combined into Single mp4 files.</i></small></pre>"
	echo "</div>"
        echo "<hr>"
	#here we are looking for conversion processes not primary stream processes
	pgrepffmpeg_func

	echo "<hr>"

	#if you want to use the HLS single_file segment option and you have it configured in channel.cmd.template as playlist.mp4
	#if single_file is enabled cut/comment starting here
	
	#note we are not overwritting here, we let each new stream creation move files down the *.playlist.mp4 chain instead.  
	#todo, Clean this up and precreate reuse variables up front

	#-bsf:a aac_adtstoasc ${i/m3u8/mp4}
	#FFCONCATCHANNEL=${i##/var/www/html/hls/}
	playlistn=0 # this is our iterate channel number for array
	#autoassign playlistn available to array 
	chplarray=($(for playlistn in $(ls -dv /var/www/html/hls/*[[:digit:]].[[:digit:]]/playlist.m3u8) ;do printf  $playlistn;printf '\n';done))
	#calc n channel playlists total
	totalchpl=$(echo ${#chplarray[@]})
	
	olrcount=0 #outer loop count
	ilrcount=0 #inner loop count
	olerrcount=0 #outer loop error count
	ilerrcount=0 #inner loop error count
	sumilerrcount=0 #sum of inner loop error resets. Each reset was 5 tries.
	#track counts errors on conversions 
	conv_errcount=0


	i=0
	if [ $olrcount -lt $totalchpl ];then 
		echo "<pre><small><i>$(for i in ${chplarray[@]};do 
		(( olrcount++ ))
	        CHANNELDIR=$(echo ${i%/*})
		m3u8_convcount=0
		concat_convcount=0
	        #get size of mp4 in megabytes
	        mp4size=$(du -m ${i/m3u8/mp4}|cut -f1)
	        #get summary size of ts files in megabytes
	        ts_size=$(du -csm $CHANNELDIR/*.ts|tail -n1|cut -dt -f1|xargs)
	        #if our previous sized mp4 is less than 95 percent of the total ts_file sizes, run again with concat
		#echo "running olrcount test here, olrcount=$olrcount"
		#echo "running totalchpl test here, totalchpl=$totalchpl"
		#echo "running conv_errcount test here, conv_errcount=$conv_errcount"
		#echo "running chplarray test here, chplarray=${chplarray[@]}"
		#echo "running iterated for chplarray test here"
	        #for  test in ${chplarray[@]};do 
		#	echo $test
		#done
		#echo "running mp4chplarray test here, mp4chplarray=${chplarray[@]/m3u8/mp4}"
	        #echo "running channeldir test here, CHANNELDIR=$(echo ${i%/*})"
		#echo "running channeldirnum test here, CHANNELDIRNUM=$(echo $(basename ${i%/*}))"
			if [ ! -s ${i/m3u8/mp4} ] && [ $m3u8_convcount -eq '0' ];then
				echo "<div class="w3-text-light-green">"
				#we run here on condition that the playlist.mp4 doesnt already exist greater than zero 
			    	#and we increment the cnts
			    	(( m3u8_convcount++ ))
				#always remove any 0 byte file, if any because can\'t overwrite it using -n below
				rm -fv ${i/m3u8/mp4} &>/dev/null
			   	echo "Playlist$olrcount INPUT_QUEUE-- $i"
			    	echo "m3u8_convcount=$m3u8_convcount"
				pgrep -x ffmpeg -u $APACHE_USER &>/dev/null
				hlsconv_retval=$?
				if [ $hlsconv_retval = '0' ];then
					echo "hlsconv_retval process reports running"
					echo "waiting, serializing processes" 
				else
					#primary fast method testing using m3u8 protocol.
			    		#kill a conversion process, if hung or if not done after 140 seconds +10, with signal 9
			    		$(timeout -k10 -s9 140 setsid ffmpeg -n -protocol_whitelist file,http,tcp -i $i -c copy ${i/m3u8/mp4} &>/dev/null&)
			    		echo "OUTPUT_QUEUE:  		 ${i%%/playlist.m3u8}/playlist.mp4"
				fi
				echo "</div>"
			elif [ -s ${i/m3u8/mp4} ] && [ $concat_convcount -eq '0' ] && [ $mp4size -lt $(( $ts_size*95/100)) ];then
				echo "<div class="w3-text-light-green">"
			    	#if mp4size than 95 percent of the total ts_file sizes, run again with concat
				(( concat_convcount++ ))
			    	echo "Playlist$olrcount INPUT_QUEUE_MP4_PRE-STAGE2:"
			        echo "--$i"
			        echo "mpeg4: ${i/m3u8/mp4} size = $mp4size Megabytes"   
			    	echo "Playlist$olrcount INPUT_QUEUE_TSFILES_PRE-STAGE2:"
			        echo "tsfiles:  ${i%/*}*.ts tsseg totals estimated = $ts_size Megabytes"   
			    	echo "m3u8_convcount=$m3u8_convcount"
			    	echo "concat_convcount=$concat_convcount"
			    	#kill any stale process just in case too
				pkill -u apache -x ffmpeg &>/dev/null
				sleep 1
				pkill -u apache -x ffmpeg &>/dev/null
				sleep .5
				pgrep -x ffmpeg -u $APACHE_USER &>/dev/null
				hlsconv2_retval=$?
				if [ $hlsconv2_retval = '0' ];then
					echo "hlsconv_retval process reports running"
					echo "waiting, serializing processes" 
				else
			    		echo "starting backup method after timeout or failure using m3u8 method"
			    		echo "creating our list from ts segments"
					echo "INPUT_QUEUE_STAGE2:"
				      	echo "${i%%playlist.m3u8}$(basename ${i%%playlist.m3u8}).tsplaylist.txt"
			    		$(printf "file '%s'\n" ${i%%playlist.m3u8}*.ts > ${i%%playlist.m3u8}/$(basename ${i%%playlist.m3u8}).tsplaylist.txt)
			    		echo "assembling segments"
					#assemble mp4 in background, timeout after 5minutes, force kill proc after 5:10seconds with signal 9
			    		setsid /usr/bin/timeout -k10 -s9 5m ffmpeg -protocol_whitelist file,http,tcp -y -f concat -safe 0 -i ${i%%playlist.m3u8}$(basename ${i%%playlist.m3u8}).tsplaylist.txt \
			       		-c copy ${i%%/playlist.m3u8}/playlist.mp4 &>/dev/null& 
			    		echo "OUTPUT_QUEUE_STAGE2:	${i%%/playlist.m3u8}/playlist.mp4"
			 		#echo "<br>"
				fi
				echo "</div>"
			elif [ -s ${i/m3u8/mp4} ] && [ -s $i ] && [ $concat_convcount -eq '0' ] && [ $m3u8_convcount -eq '0' ] ;then
				#pgrepffmpeg_func
				echo "<div class="w3-text-evergreen">"
			    	#echo "retval=$retval" 
			    	#echo "retvalffmpeg=$retvalffmpeg" 
			    	if [ $retvalffmpeg -eq '1' ];then
					echo "Playlist$olrcount -- $i  CONVERTED to mp4" 
			    	fi
				#    echo "m3u8_convcount=$m3u8_convcount"
				#    echo "concat_convcount=$concat_convcount"
				#    echo "m3u8_convcount=$m3u8_convcount"
				#    echo "outer loop run count=$olrcount"
				#    echo "conversion error count=$conv_errcount"
				echo "</div>"
			else
				echo "<div class="w3-text-red">"
			    	echo "outer loop run count=$olrcount"
			    	echo "conversion error count=$conv_errcount"
			    	echo "Undefined condition"
			    	echo "Incrementing conv_errount +1"
	       		    	(( conv_errcount++ ))
				echo "</div>"
			fi
		done 2>/dev/null)</i></small></pre>"
	else
		echo "No playlist.m3u8 files found. Fresh install?"
	fi	
	#if you want to use the HLS single_file segment option and you have it configured in channel.cmd.template as playlist.mp4
	#if single_file is enabled stop cut/commenting here
	unset i
	echo "<hr>"
	echo "<div class="w3-text-grey">"
	echo "<pre>$(uptime)</pre>"
	echo "</div>"
	i=0
	echo "<div class="w3-text-orange">"
	echo "<pre><small><i>$(for i in $(cat /sys/class/thermal/thermal_zone{0..9}/{type,temp} 2>/dev/null);do printf $i'\n';done)</i></small></pre>"
	echo "</div>"
        echo "<pre><b>Remaining Disk Space Available:</b> $(df -lh /var/www/html/hls|awk '{print $4}'|tail -n1)</pre>"
	echo "<b>HLS Directory Sizes</b>"
	echo "<small>"
	echo "<pre><i>$(find /var/www/html/hls -type d -iname '*[[:digit:]].[[:digit:]]' -not -empty -printf '%p \t' -exec bash -c 'du -sh $0|cut -d/ -f1' {} \;)</i></pre>"
	echo "</small>"
	#echo "<pre><b>Mp4 Stream Durations;Hours:Minutes:Seconds</b></pre>"
	#echo "<small>"
	#this can be slow 
	#echo "<pre>$(find /var/www/html/hls/ -type f -iname "*playlist.mp4" -not -empty -printf '%p      \t' -exec bash -c '/usr/bin/ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 -sexagesimal $0' {} \;|cut -d. -f1-3)</pre>"
	#echo "</small>"
	echo "<div class="w3-text-grey">"
	echo "<pre><small><i>$(uname -a)</i></small></pre>"
	echo "</div>"
	echo "</div>"
	echo "</h4>"
	echo "<footer></footer>"
	echo "</body></html>"
	exit 0
else
	#this filter is fairly good to catch the process and digits
	SCHANNEL=$(ps -f -p$(pgrep -d, -u $APACHE_USER -x hls_stream_hdhr)|awk '{print $10}'|cut -dv -f2|cut -d? -f1|grep -Eo '([0-9]{1,2}\.[0-9]{1,2})'|xargs)
	echo "<h4>"
	echo "<hr>"
	echo "<div class="w3-text-cyan">"
	echo "<div style="text-align:left">"
	echo "<pre><small><i>$(ps -C hls_stream_hdhr -o lstart,user,pid,ppid,%cpu,%mem,cmd --width 500)</i></small></pre>"
	echo "</div>"
	echo "</div>"
	echo ""
	PID=$(ps -C hls_stream_hdhr -o pid= )
	SCHANNELSTARTED=$(ps -C hls_stream_hdhr -o lstart=)
	
	#time now in epoc
	EPOCNOW=$(date +"%s")
	
	#when stream started for $SCHANNEL
	SEPOC=$(date -d "$(echo $SCHANNELSTARTED)" +"%s")
		
	#how long stream running in total seconds since started
	SEPOCSECS=$(let "SEPOCSECS = $EPOCNOW - $SEPOC";echo $SEPOCSECS)
	
	#total seconds stream running /60# for minutes
	SRUNTIME=$(let "SRUNTIME =  $SEPOCSECS/60";echo $SRUNTIME)
	echo "<div class="w3-text-aqua">"
	if [ $SEPOCSECS -lt 120 ];then
		echo "<pre>hls_stream ~ Runtime: $(echo $SEPOCSECS) Seconds</pre>"
	else 	
		echo "<pre>hls_stream ~ Runtime: $(echo $SRUNTIME) Minutes</pre>"
	fi	
	echo "</div>"
	echo "<hr>"
	if [ ! -z $SCHANNEL ];then 
		echo "<div style="text-align:center">"
		echo "<form action="/cgi-bin/kill-hls_stream_hdhr.cgi">"
		echo "<input type="submit" value='<STOP>  Streaming Ch $SCHANNEL' class="button0" />"
		echo "</form>"
		echo "<hr>"
		echo "<br>"
		#echo "<pre><b>$(echo SCHANNEL=$SCHANNEL)</b></pre>"
		echo "<a target="_blank" rel="noopener noreferrer" href="$HTTP_HLSDIR/$SCHANNEL/playlist.m3u8" class="button"><\Watch/>  Ch $SCHANNEL</a>"
	else
		echo "<pre><b>Note Showing Null Channel Value</pre>"
	fi

	echo "<div class="w3-text-grey">"
	echo "<pre><b>$(uptime)</b></pre>"
	echo "</div>"
	echo "<div class="w3-text-orange">"
	echo "<pre><small><i>$(for i in $(cat /sys/class/thermal/thermal_zone{0..9}/{type,temp} 2>/dev/null);do printf $i'\n';done)</i></small></pre>"
	echo "</div>"
        echo "<pre><b>Remaining Disk Space Available:</b> $(df -lh /var/www/html/hls|awk '{print $4}'|tail -n1)</pre>"
	echo "<b>HLS Directory Sizes</b>"
	echo "<small>"
	echo "<pre><i>$(find /var/www/html/hls -type d -iname '*[[:digit:]].[[:digit:]]' -not -empty -printf '%p \t' -exec bash -c 'du -bsh $0|cut -d/ -f1' {} \;)</i></pre>"
	echo "</small>"
	echo "<div class="w3-text-grey">"
	echo "<pre><small><i>$(uname -a)</i></small></pre>"
	echo "</div>"
	echo "</div>"
	echo "</h4>"
	echo "<footer></footer>"
	echo "</body></html>"
	exit 0
fi
