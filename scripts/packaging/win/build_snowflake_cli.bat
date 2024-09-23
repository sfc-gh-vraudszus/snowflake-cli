@echo off
set PATH=C:\Program Files\Python310\;c:\Program Files (x86)\Windows Kits\8.1\bin\x86\;%PATH%

python.exe --version
python.exe -c "import platform as p; print(f'{p.system()=}, {p.architecture()=}')"

python.exe -m pip install --upgrade pip uv hatch

@echo off
FOR /F "delims=" %%I IN ('hatch run packaging:win-build-version') DO SET CLI_VERSION=%%I
echo %CLI_VERSION%

set ENTRYPOINT=src\\snowflake\\cli\\_app\\__main__.py

RMDIR /S /Q dist
RMDIR /S /Q build
DEL /Q *.wixobj

@echo on
python.exe -m hatch -e packaging run ^
  pyinstaller ^
  --target-arch=64bit ^
  --name snow ^
  --onedir ^
  --clean ^
  --noconfirm ^
  --console ^
  --icon=scripts\packaging\win\snowflake_msi.ico ^
  %ENTRYPOINT%

tar -a -c -f snowflake-cli-%CLI_VERSION%.zip dist\snow


heat.exe dir dist\\snow\\_internal ^
  -gg ^
  -cg SnowflakeCLIInternalFiles ^
  -dr TESTFILEPRODUCTDIR ^
  -var var.SnowflakeCLIInternalFiles ^
  -sfrag ^
  -o _internal.wxs

candle.exe ^
  -arch x64 ^
  -dSnowflakeCLIVersion=%CLI_VERSION% ^
  -dSnowflakeCLIInternalFiles=dist\\snow\\_internal ^
  scripts\packaging\win\snowflake_cli.wxs ^
  scripts\packaging\win\snowflake_cli_exitdlg.wxs ^
  _internal.wxs

light.exe ^
  -ext WixUIExtension ^
  -ext WixUtilExtension ^
  -cultures:en-us ^
  -loc scripts\packaging\win\snowflake_cli_en-us.wxl ^
  -out snowflake-cli-%CLI_VERSION%-x86_64.msi ^
  snowflake_cli.wixobj ^
  snowflake_cli_exitdlg.wixobj ^
  _internal.wixobj
