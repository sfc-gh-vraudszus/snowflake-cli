@echo on
echo %PATH%
"C:\Program Files\Python310\python.exe" --version
"C:\Program Files\Python310\python.exe" -m pip install --upgrade pip uv hatch

set PATH = C:\Program Files\Python310\;%PATH%
echo %PATH%
python.exe --version
python.exe -m pip install --upgrade pip uv hatch

REM @echo off
FOR /F "delims=" %%I IN ('python.exe -m hatch version') DO CLI_VERSION=%%I
echo %CLI_VERSION%
REM @echo on

REM @echo off
set CONTENTSDIR="snowflake-cli-%CLI_VERSION%"
set ENTRYPOINT=src\\snowflake\\cli\\_app\\__main__.py
python.exe -m hatch -e packaging run pyinstaller --name snow --onedir --clean --noconfirm --noconsole --contents-directory=%CONTENTSDIR% %ENTRYPOINT%

cd dist
dir .
REM signtool sign /debug /sm /t http://timestamp.digicert.com /a snow.exe
wmic product get name, version


REM candle /?
REM light /?
