call %USERPROFILE%\Envs\scripts\Scripts\activate.bat
chcp 65001
python %USERPROFILE%\Dropbox\Reference\S\scripts\demux.py %*
pause
