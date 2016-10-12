chcp 65001
call %USERPROFILE%\Env\scripts\Scripts\activate.bat
python %USERPROFILE%\Dropbox\Reference\S\scripts\demux.py %*
pause