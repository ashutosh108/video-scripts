call %USERPROFILE%\Envs\scripts\Scripts\activate.bat
chcp 65001
python %~dpn0.py %*
pause
