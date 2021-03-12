I tested a regular 4 tuner hdhr(HDHR5-4US) with a raspberrypi 4 using raspbian 32bit
```
Raspberry Pi reference 2019-09-26
Generated using pi-gen, https://github.com/RPi-Distro/pi-gen, 80d486687ea77d31fc3fc13cf3a2f8b464e129be, stage5

(debian_version 10.7).
```

After testing I added new options for use with regular hdhrs to the channelcmd.template.cgi file, for those that dont have hw transcoding already in the ts stream.
```
Just change the default one from FFOUTVCODE=copy to FFOUTVCODEC="h264_v4l2m2m -b:v 8M" or FFOUTVCODEC="h264_omx -b:v 8M" 
*only choose one option and rem other out.
```


#on debian after changing vcodec to h264_v4l2m2m, you may need to set up permissions for the apache user to access the v4l2 device
```
#usermod -aG audio,video www-data    

```
#on centos
```
#usermod -aG audio,video apache

```

#TBD h264_omx may need user options set as well.
