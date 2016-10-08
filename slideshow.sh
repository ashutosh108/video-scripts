mogrify -resize 1280x720 -gravity center -extent 1280x720 -background black -path q *.jpg
ffmpeg -i "2016-10-01 goswamimj_rus_stereo.mp3" -loop 1 -framerate 1/10 -i "2016-10-01 goswamimj %d.jpg" -c:v libx264 -r 15 -pix_fmt yuv420p -c:a copy -shortest "2016-10-01 goswamimj_rus_stereo.mp4"
