pyinstaller console_start.py --path="%cd%\Scripts" -F -n validator
del /f validator.exe validator.spec
copy "%cd%\dist\validator.exe" "%cd%\validator.exe"
rd "%cd%\dist" "%cd%\build" /S /Q
