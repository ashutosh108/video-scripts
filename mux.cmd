rem @echo off
rem switch to UTF-8
chcp 65001
goto MAIN

:USAGE_EXIT
echo mux eng/rus audio files into a Goswami Maharaj's video
echo usage: mux "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)
goto :EXIT

:MAIN
IF z%1z==zz GOTO USAGE_EXIT

call C:\Users\ashutosh\Envs\scripts\Scripts\activate.bat
echo on

set ss_arg=
set /p offset=<"%~dpn1_offset.txt"
if [%offset%] == [] GOTO SKIP_SS
set ss_arg=-ss %offset%
:SKIP_SS

set title_pre=%~n1
set title=%title_pre: goswamimj=%

REM -movflags +faststart means make file stream-optimized: write the 'moov' atom at the file start
rem D:\video\GoswamiMj-videos\ffmpeg-hi8-heaac.exe ^
rem ffmpeg ^
rem     -map 0:a ^
rem     -c:a:1 copy -metadata:s:a:1 language=eng ^

start call C:\Users\ashutosh\Dropbox\Reference\S\scripts\mux_rus_stereo.cmd %1

D:\video\GoswamiMj-videos\ffmpeg-hi8-heaac.exe ^
    -y ^
    -i "%~dp1temp\%~n1_rus_mixdown.wav" ^
    -c:a libfdk_aac -ac 1 -b:a 128k -metadata:s:a:0 language=rus ^
    -movflags +faststart ^
    -metadata artist="Бхакти Судхир Госвами" ^
    -metadata title="%title% (моно)" ^
    -metadata album="Гупта Говардхан 2016" ^
    "%~dp1temp\%~n1_rus_mono.m4a"

ffmpeg ^
    -y ^
    -i %1 -i "%~dp1temp\%~n1_rus_mono.m4a" ^
    -map 0:v ^
    -map 1:a ^
    -c copy ^
    -movflags +faststart ^
    -metadata artist="Бхакти Судхир Госвами" ^
    -metadata title="%title% (моно)" ^
    -metadata album="Гупта Говардхан 2016" ^
    %ss_arg% ^
    "%~dp1temp\%~n1_rus_mono.mp4"
python C:\Users\ashutosh\Dropbox\Reference\S\scripts\upload_video.py --file "%~dp1temp\%~n1_rus_mono.mp4"
pause
rem    -map 1:a ^
rem    -codec:a mp3 -b:a 128k ^
rem    "%~dpn1_rus.mp3"

:EXIT