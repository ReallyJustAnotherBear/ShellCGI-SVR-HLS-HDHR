 **** This document was written when using with a silicondustTM hdhr-extend using in USA with ATSC 8VSB OTA, this part should still work for non-transcode models as well. 

****For using with DVB see "DVBwork.md"

  
#####
### This will be automated later as part of setup.sh

#### Before starting
#### Edit your http.conf section on your distro and make sure you have your apache server/cgi-bin setup properly and working.
#### use a test script from your distro prior to starting this.








### Make sure you have already installed 'curl,sed and xmlstarlet' in your distro.
### You will need to scan for channels on your hdhr from its web interface by ip by going to its ip/lineup.html
#eg.
#
```
http://HDHR_IP/lineup.html
```

## Choose Detect Channels if the channels are not populated already.
#<screenshot>


## *dl channels >channels.txt #note we are removing any channels that dont have a period, which means we filter those that don't have listed subchannels.
### Note port is usually on 80 unless your forwarding to something else 
```
curl  -s http://$HDHR_IP/lineup.xml|xmlstarlet sel -t -v "//GuideNumber"|sed '/\./!d'>/var/www/html/channels.txt
```


### View the channels.txt and optionally then edit/remove any you don't want to use
```
cat ../channels.txt
```

## channels need mapped from channels.txt to channel names. The main cgi script "channelcmd.template" is to be used to create your channel names be either linked with hardlinks or copied(not preferred) to your cgi-bin directory location: 

  What happens when you use links is you can edit only the main file then that represents each channel, all of them are updated if you use hardlinks. Using individual files for each channel is only recommended if you want to have different ffmpeg options per channel. eg. If you wanted to have audio stream 2 from a channel you could change it on 1 with multiple channel files and it would choose that as the default stream. 
  Another way to do it. You can still customize without using hardlinks for them all as well and do so by deleting a channel link and copying from the 'channelcmd.template' file to a new file/channelname. This gives you two files to maintain in this scenario for channels, all those hardlinked and the one you copied for a customizable channel.**LATER IDEA(Perhaps later buttons or slides for these options in the web interface would be nice. 

### Need the channels.txt parsed to create the links since most people will want to startout simple and only edit one channel file that updates them all.
### So once your satisfied with the channels you will be using, make links from the channel file(channelcmd.template) to new channel names sourcing the channels.txt. Simplier than it sounds.

```
#on centos path is
cd /var/www/cgi-bin/

####  on debian change to cgi-bin path
```
cd /usr/lib/cgi-bin/
```

```

#### cat the channels.txt created earlier and make links in current cgi-bin directory from files contents/channels.
```
for i in $(cat /var/www/html/channels.txt);do ln -v channelcmd.template.cgi $i.cgi ; done
```


#### Now if you check you should have channels  in the format'XX.x'/'XXX.x' created as links to the channelcmd.template file all with same size
```
ls -al 
```

#### notice all the channels have the excact same filesize from the hardlinking as the channelcmd.template
#### if you look at inodes you will these files we just created all point to same inode

#### Once your done setting up your channel scripts you need to create directories in :html/hls for each channel name/number
#### On both debian/centos go to /var/www/html and create a new diretory labeled hls and go to it

```
mkdir -v /var/www/html/hls
cd /var/www/html/hls
```


#### now we reference the channels file again and create directories instead of links from it.
```
for i in $(cat /var/www/html/channels.txt);do mkdir -v $(echo $i.cgi|cut -d. -f1,2) ; done
```



#### Example from my case
```
root@debian:/var/www/html/hls# for i in $(cat /var/www/html/channels.txt);do mkdir -v $(echo $i.cgi|cut -d. -f1,2) ; done
mkdir: created directory '9.1'
mkdir: created directory '9.2'
mkdir: created directory '9.3'
mkdir: created directory '13.1'
mkdir: created directory '13.2'
mkdir: created directory '13.3'
mkdir: created directory '16.1'
mkdir: created directory '16.2'
mkdir: created directory '16.3'
mkdir: created directory '23.1'
mkdir: created directory '23.2'
mkdir: created directory '28.1'
mkdir: created directory '28.2'
mkdir: created directory '28.3'
mkdir: created directory '28.4'
mkdir: created directory '34.1'
mkdir: created directory '34.2'
```

#### Now your ready to edit a few files in the CGI-BIN directory.
#### Which I will later put in another document ###ManualSetupPartX


####  update IP/HOSTNAME in both :HDHR_IP.sh and HLS_SERVER_IP.sh files  
####  update XYZ file.sh with your CGI-BIN path for your distro







#### When finished make sure to chown cgi-bin and html dirs as 'www-data' for debian, 'apache' for centos
#### and chmod -R 0755 cgi-bin/* html/*




