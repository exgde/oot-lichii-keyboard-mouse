@echo off
rem Applies OoT-Keyboard-Mouse-Settings.ini to Lichii. Close Lichii first.
rem This is a plain text file: you can open it in Notepad to see what it does.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Apply-Settings.ps1" %*
echo.
pause
