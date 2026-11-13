@echo off
rem Installs the OOT keyboard + mouse mod into Lichii. Close Lichii first.
rem This is a plain text file: you can open it in Notepad to see what it does.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install.ps1" %*
echo.
pause
