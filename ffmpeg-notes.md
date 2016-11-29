Single jpg with mp3 for youtube
===============================

~70x encoding speed (i3 550 3.2GHz)
Resizing is meant to ask youtube to keep higher-quality audio (rumours are that 720p and higher gets better audio in youtube)
ffmpeg -loop 1 -r 1 -i "2016-11-28 goswamimj.jpg" -i "2016-11-28 goswamimj.mp3" -c:v h264_nvenc -c:a copy -shortest -pix_fmt yuv420p -tune stillimage -vf "scale=iw*min(1280/iw\,720/ih):ih*min(1280/iw\,720/ih),pad=1280:720:(1280-iw)/2:(720-ih)/2" "2016-11-28 goswamimj.mkv"

# -preset ultrafast 

Use NVIDIA videocard for encoding
=================================

-c:v h264_nvenc (and remove -preset ultrafast)

Loudness normalization (EBU R128)
=================================
-af loudnorm=I=-16:TP=-1
LUFS = -16 and target peak = -1 are seems to be recommended for mobile content:
https://auphonic.com/blog/2013/01/07/loudness-targets-mobile-audio-podcasts-radio-tv/
http://www.aes.org/technical/documents/AESTD1004_1_15_10.pdf

combine mp4 from facebook with our normal livestream mp4
========================================================
rem    -i "2016-09-14 goswamimj_BhaktivinodApp.png" ^
ffmpeg ^
    -i "D:\video\GoswamiMj-videos\2016-09-14 goswamimj_BhaktivinodApp-facebook.mp4" ^
    -r 29.970297 ^
    -ar 44100 ^
    -b:a 128k ^
    -t 3:24.661 ^
    -vf scale=-1:450,pad=800:450:(ow-iw)/2:(oh-ih)/2 ^
    -pix_fmt yuv420p ^
    -ac 1 ^
    "2016-09-14 goswamimj_BhaktivinodApp-still.mp4"

Picture resizing in general case
================================
-vf "scale=min(iw*TARGET_HEIGHT/ih\,TARGET_WIDTH):min(TARGET_HEIGHT\,ih*TARGET_WIDTH/iw),pad=TARGET_WIDTH:TARGET_HEIGHT:(TARGET_WIDTH-iw)/2:(TARGET_HEIGHT-ih)/2"
for example:
-vf "scale=iw*min(1280/iw\,720/ih):ih*min(1280/iw\,720/ih),pad=1280:720:(1280-iw)/2:(720-ih)/2"

Slideshow from multiple jpg files
=================================

1. resize jpgs
    mogrify -resize 1280x720 -gravity center -extent 1280x720 -background black -path q *.jpg

2. combine jpgs with mp3:
    ffmpeg -i "2016-10-01 goswamimj_rus_stereo.mp3" -loop 1 -framerate 1/10 -i "2016-10-01 goswamimj %d.jpg" -c:v libx264 -r 15 -pix_fmt yuv420p -c:a copy -shortest "2016-10-01 goswamimj_rus_stereo.mp4"

How to do "Ducking" to turn down original's volume when the translator is speaking
==================================================================================

On the original track you add a Dynamics processor and enable stereo side-chain.
On the translation track you send the audio to the side-chain on the compressor.
https://www.youtube.com/watch?v=kMk0XUCUkDY