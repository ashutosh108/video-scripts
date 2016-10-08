REM concat:
ffmpeg -i "D:\video\GoswamiMj-videos\2016-09-14 goswamimj_BhaktivinodApp-still.mp4" -c copy -bsf:v h264_mp4toannexb -f mpegts temp1.ts
ffmpeg -i "D:\video\GoswamiMj-videos\2016-09-14 goswamimj_BhaktivinodApp-livestream.mp4" -c copy -bsf:v h264_mp4toannexb -f mpegts temp2.ts
ffmpeg -i "concat:temp1.ts|temp2.ts" -c copy -bsf:a aac_adtstoasc "2016-09-14 goswamimj_BhaktivinodApp.mp4"
