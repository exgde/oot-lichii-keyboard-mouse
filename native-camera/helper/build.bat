@echo off
rem Builds OoT-MouseCapture.exe with the Visual Studio C compiler (Build Tools are enough).
rem Run from "x64 Native Tools Command Prompt for VS", or let it find vcvars64.bat below.
where cl >nul 2>&1 || call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
cd /d "%~dp0"
cl /nologo /O2 /MT /W4 /D_CRT_SECURE_NO_WARNINGS mouse_capture.c /Fe:OoT-MouseCapture.exe user32.lib winmm.lib /link /SUBSYSTEM:CONSOLE
del /q mouse_capture.obj 2>nul
