#### CHECKSUMS_CONCEPTS.md

Since this is a shell scripts project, take the checksums of all binaries used on local OS on first setup.cgi, install.

eg. 
```
for i in which $(sha1sum ffmpeg cut);do echo $i;done

sha1sum -b $(ffmpeg) > $CGI-BIN/ffmpeg.sha1sum
sha1sum -b $(which sha1sum) > $CGI-BIN/sha1sum.sha1sum
