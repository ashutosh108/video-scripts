import os
import subprocess

os.environ['FONTCONFIG_FILE'] = 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\\scripts\\fonts\\fonts.conf'
try:
    os.remove('qwe.mp4')
except:
    pass
try:
    os.remove('qwe.png')
except:
    pass


def MakeEnTitlePng():
    f_goswami = 'drawtext=font=Charis SIL' + \
                ':text=Śrīla Bhakti Sudhīr Goswāmī Mahārāja' + \
                ':fontcolor=white' + \
                ':fontsize=36' + \
                ':x=(w-tw)/2:y=h-150'
    f_title = 'subtitles=filename=qwe.srt:force_style=\'FontName=Charis SIL,Fontsize=108,Alignment=10,PlayResX=1280,PlayResY=720,PrimaryColour=&Hffffff\''
    f_shift_up = 'crop=1280:720-50:0:50,pad=1280:720:0:0:color=black@0.0'
    f_transparent = 'geq=r=r(X\,Y):a=if(r(X\,Y)\,r(X\,Y)\,122)'
    filter_complex = ''
    filter_complex += ',' + f_title
    filter_complex += ',' + f_shift_up
    filter_complex += ',' + f_goswami
    filter_complex += ',' + f_transparent
    filter_complex = filter_complex[1:]
    args = ['ffmpeg',
            '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:d=10,format=rgba',
            '-filter_complex', filter_complex,
            '-frames:v', '1',
            '-y', 'qwe.png'
            ]
    subprocess.run(args)


MakeEnTitlePng()

filter_complex = ''
filter_complex += ';[1:v]fade=out:st=9:d=1:alpha=1[title]'
filter_complex += ';[0:v][title]overlay,format=yuv420p'
# filter_complex += ';[title]null[out]'
# filter_complex += ';[0:v]format=rgba,drawbox=0:0:1280:720:color=black@0.4:t=max,overlay'
# filter_complex += ';[v0]null[v0fade]'
# filter_complex += ';[2:v]null[v1fade]'
# filter_complex += ';[v0]format=pix_fmts=yuva420p,fade=out:st=1:d=2:alpha=1[v0fade]'
# filter_complex += ';[2:v]format=pix_fmts=yuva420p,fade=in:st=1:d=2:alpha=1[v1fade]'
# filter_complex += ';[3:v][v0fade]overlay[over]'
# filter_complex += ';[over][v1fade]overlay'
filter_complex = filter_complex[1:]
args = ['ffmpeg',
        '-ss', '1:15', '-i', '2017-01-25 goswamimj.mp4',
        '-loop', '1', '-i', 'qwe.png',
        '-filter_complex', filter_complex,
        '-y',
        # '-map', '[out]',
        # '-frames:v', '1',
        # '-v', 'debug',
        '-t', '10',
        'qwe.mp4']

subprocess.call(args)
subprocess.call(['C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe', '--sub-track-id=99', 'qwe.mp4'])
# subprocess.run('start qwe.png', shell=True)

# CHCP 65001
# rem set filter="[1:v]drawtext=font=Charis SIL:text=Śrīla Bhakti Sudhīr Goswāmī Mahārāja:fontcolor=white:fontsize=36:x=(w-tw)/2:y=h-150[t],[t][0:v]overlay"
# set filter=[1:v]drawtext=font=Charis\ SIL:text=qwe[t]
# set filter=%filter%,[t][0:v]overlay
# ffmpeg ^
# 	-ss 1:15 -i "2017-01-25 goswamimj.mp4" ^
# 	-f lavfi -i nullsrc=s=1280x720:d=10 ^
# 	-filter_complex %filter% ^
# 	-map 0:a ^
# 	-t 5 ^
# 	-y qwe.mp4
# pause
# rem -ss 0:01:15 -i "2017-01-25 goswamimj.mp4" ^
# rem 	-vf "drawbox=x=0:y=0:color=black@0.4:width=iw:height=ih:t=max,subtitles=filename=qwe.srt:force_style='FontName=Charis SIL,Fontsize=108,Alignment=10,PlayResX=1280,PlayResY=720,MarginV=0',drawtext=font=Charis SIL:text=Śrīla Bhakti Sudhīr Goswāmī Mahārāja:fontcolor=white:fontsize=36:x=(w-tw)/2:y=h-150,crop=1280:720-50:0:50,pad=1280:720" ^
# rem drawbox=x=0:y=0:color=black@0.4:width=iw:height=ih:t=max
# rem subtitles=filename=qwe.srt:force_style='FontName=Charis SIL,Fontsize=108,Alignment=10,PlayResX=1280,PlayResY=720'
# rem drawtext=font=Charis SIL:text=Śrīla Bhakti Sudhīr Goswāmī Mahārāja:fontcolor=white:fontsize=36:x=(w-tw)/2:y=h-150
# rem crop=1280:720-50:0:50,pad=1280:720
