#!/bin/bash
# (c) 2021-01-12 Kelsie Flynn
# License MIT
#install3.cgi
echo "Content-type: text/html"
echo ""
echo "<link rel="stylesheet" type="text/css" href="/w3.css">"
echo "<html>"
echo "<head>"
echo "<title>HLS Live Installer page3</title>"
echo "<style>"
echo ".button0 {color:black;background-color:red;width:50%;font-size:32px;padding:4px 2px;border-radius:24px;text-decoration:none}"
echo ".button {color:black;background-color:lime;font-size:64px;padding:1px 18%;border:2px solid black;text-decoration:none;border-radius:96px}"
echo "body {
  background-color: black;
  color: green;
}"
echo "h2 {text-align: center;}"
echo "pc {text-align: center;}"
echo "p {text-align: left;}"
echo "div {text-align: center;}"
echo "</style>"
echo "</head>"
echo "<body>"
echo "<header>"
echo "</header>"
echo "<br>"
echo "<br>"
echo "<div>"
echo "<h2>FFmpeg Default Video output Codec</h2>"
echo "<hr>"
echo '<form action="/cgi-bin/INSTALL/setupffoutvcodec.cgi" method="post">
<div style="display: inline-block; text-align: left;">

<input type="radio" id="copy" name="FFOUTVCODEC" value="copy">
	<label for="copy">copy -->*For Sources already in mp4</label><br>

<input type="radio" id="libx264" name="FFOUTVCODEC" value="libx264">
	<label for="libx264">libx264 -->*Software Only using ffmpeg and CPU(s)</label><br>

<input type="radio" id="rpi-omx" name="FFOUTVCODEC" value="h264_omx">
	<label for="rpi-omx">h264_omx -->*RaspberryPi OMX</label><br>

<input type="radio" id="h264_v4l2m2m" name="FFOUTVCODEC" value="h264_v4l2m2m">
	<label for="h264_v4l2m2m">h264_v4l2m2m -->*Linux V4L2 Mem 2 Mem Interface</label><br>

<input type="radio" id="intel-qsv" name="FFOUTVCODEC" value="h264_qsv">
	<label for="intel-qsv">h264_qsv -->*Intel QSV</label><br>

<input type="radio" id="nvidia-nvenc" name="FFOUTVCODEC" value="h264_nvenc">
	<label for="nvidia-nvenc">h264_nvenc -->*NVIDIA nvenc</label><br><br>

<input type="submit" value="Submit">
</div></form>'

echo "</div>"

echo "</body></html>"

