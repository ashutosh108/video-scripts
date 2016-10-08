rem @echo off
goto MAIN

:USAGE_EXIT
echo mux eng/rus audio files into a Goswami Maharaj's video
echo usage: mux "yyyy-mm-dd goswamimj.mp4"
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
rem D:\video\GoswamiMj-videos\ffmpeg-hi8-heaac.exe ^
rem ffmpeg ^
ffmpeg ^
    -y ^
    -i %1 ^
    -c copy ^
    -movflags +faststart ^
    -metadata artist="Bhakti Sudhir Goswami" ^
    -metadata title="%title%" ^
    -metadata album="Gupta Govardhan 2016" ^
    %ss_arg% ^
    "%~dp1temp\%~n1_eng.mp4"
pause
rem    -map 1:a ^
rem    -codec:a mp3 -b:a 128k ^
rem    "%~dpn1_rus.mp3"

:EXIT