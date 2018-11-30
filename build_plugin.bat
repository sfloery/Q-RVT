REM @echo off
REM call "C:\Program Files\QGIS 3.2\bin\o4w_env.bat"
REM call "C:\Program Files\QGIS 3.2\bin\qt5_env.bat"
REM call "C:\Program Files\QGIS 3.2\bin\py3_env.bat"

REM @echo on
REM pyrcc5 -o resources.py resources.qrc

echo %cd%
xcopy /s %cd% C:\Users\sfloe\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\qrvt
