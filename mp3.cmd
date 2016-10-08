rem @echo off
rem switch to UTF-8
chcp 65001
goto MAIN

:USAGE_EXIT
echo mp3: encode rus audio track for Goswami Maharaj's video from wav to mp3
echo usage: mp3 "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)
goto :EXIT

:MAIN
IF z%1z==zz GOTO USAGE_EXIT

set ss_arg=
set /p offset=<"%~dpn1_offset.txt"
if [%offset%] == [] GOTO SKIP_SS
set ss_arg=-ss %offset%
:SKIP_SS

set title_pre=%~n1
set title=%title_pre: goswamimj=%

REM -movflags +faststart means make file stream-optimized: write the 'moov' atom at the file start

start ffmpeg ^
    -y ^
    -i "%~dp1temp\%~n1_rus_mixdown.wav" ^
    -codec:a mp3 ^
    -b:a 128k ^
    %ss_arg% ^
    -metadata artist="Бхакти Судхир Госвами" ^
    -metadata title="%title%" ^
    -metadata album="Гупта Говардхан 2016" ^
    "%~dp1temp\%~n1_rus_stereo.mp3"

start ffmpeg ^
    -y ^
    -i "%~dp1temp\%~n1_rus_mixdown.wav" ^
    -codec:a mp3 ^
    -ac 1 ^
    -b:a 96k ^
    %ss_arg% ^
    -metadata artist="Бхакти Судхир Госвами" ^
    -metadata title="%title% (моно)" ^
    -metadata album="Гупта Говардхан 2016" ^
    "%~dp1temp\%~n1_rus_mono.mp3"

ffmpeg ^
    -y ^
    -i "%~dp1temp\%~n1.m4a" ^
    -ac 1 ^
    -codec:a mp3 -b:a 96k ^
    %ss_arg% ^
    -metadata artist="Bhakti Sudhir Goswami" ^
    -metadata title="%title%" ^
    -metadata album="Gupta Govardhan 2016" ^
    "%~dp1temp\%~n1_eng.mp3"
pause

:EXIT