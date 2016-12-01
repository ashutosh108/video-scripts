call %USERPROFILE%\Envs\scripts\Scripts\activate.bat
chcp 65001
start pythonw %~dpn0.py %*
