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
