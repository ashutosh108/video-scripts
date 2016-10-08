rem @echo off
goto MAIN

:USAGE_EXIT
echo extract (demux) english AAC audio from Goswami Maharaj's video into separate m4a file
echo usage: demux "yyyy-mm-dd goswamimj.mp4"
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

ffmpeg ^
    -y ^
    -i %1 ^
    -map 0:a -c:a copy -movflags +faststart %ss_arg% ^
    -metadata artist="Bhakti Sudhir Goswami" ^
    -metadata title="%title%" ^
    -metadata album="Gupta Govardhan 2016" ^
    "%~dp1temp\%~n1_eng.m4a" ^
    -map 0:a -c:a copy -movflags +faststart          "%~dp1temp\%~n1.m4a"
pause

:EXIT