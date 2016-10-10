call C:\Users\ashutosh\Envs\scripts\Scripts\activate.bat
rem switch to UTF-8
chcp 65001

set ss_arg=
set /p offset=<"%~dpn1_offset.txt"
if [%offset%] == [] GOTO SKIP_SS
set ss_arg=-ss %offset%
:SKIP_SS

set title_pre=%~n1
set title=%title_pre: goswamimj=%

D:\video\GoswamiMj-videos\ffmpeg-hi8-heaac.exe ^
    -y ^
    -i %1 -i "%~dp1temp\%~n1_rus_mixdown.wav" ^
    -map 0:v ^
    -c:v copy ^
    -map 1:a ^
    -c:a:0 libfdk_aac -b:a 384k -metadata:s:a:0 language=rus ^
    -movflags +faststart ^
    -metadata artist="Бхакти Судхир Госвами" ^
    -metadata title="%title%" ^
    -metadata album="Гупта Говардхан 2016" ^
    %ss_arg% ^
    "%~dp1temp\%~n1_rus_stereo.mp4"
if errorlevel 1 goto EXIT
python C:\Users\ashutosh\Dropbox\Reference\S\scripts\upload_video.py --file "%~dp1temp\%~n1_rus_stereo.mp4"
:EXIT
pause
