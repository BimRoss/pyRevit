@echo off
setlocal ENABLEDELAYEDEXPANSION
set parentpath=%AppData%\pyRevit
set filename=%parentpath%\pyRevit_config.ini

if not exist %parentpath%\ mkdir %parentpath%

echo.>%filename%

echo [core]>%filename%
echo checkupdates = False>>%filename%
echo verbose = True>>%filename%
echo debug = False>>%filename%
echo filelogging = True>>%filename%
echo startuplogtimeout = 10>>%filename%

set pa=%APPDATA%\pyRevitExtensions
set pa=%pa:\=\\%

echo userextensions = ['%pa%']>>%filename%
echo compilecsharp = True>>%filename%
echo compilevb = True>>%filename%
echo loadbeta = False>>%filename%
echo rocketmode = False>>%filename%

set pb=%APPDATA%\pyRevit\pyRevit-v45\pyRevit\pyrevitlib\pyrevit\output\outputstyles.css
set pb=%pb:\=\\%

echo outputstylesheet = %pb%>>%filename%
echo bincache = True>>%filename%
echo minhostdrivefreespace = 0>>%filename%
echo requiredhostbuild = 0>>%filename%

echo.>>%filename%

echo [usagelogging]>>%filename%
echo active = TRUE>>%filename%
echo logfilepath = >>%filename%
REM echo logserverurl = 

echo.>>%filename%

echo [pyRevitDevTools.extension]>>%filename%
echo disabled = True>>%filename%
echo private_repo = True>>%filename%
echo username = >>%filename%
echo password = >>%filename%

echo.>>%filename%

echo [pyRevitTools.extension]>>%filename%
echo disabled = False>>%filename%
echo private_repo = True>>%filename%
echo username = >>%filename%
echo password = >>%filename%

echo.>>%filename%

echo [pyRevitTutor.extension]>>%filename%
echo disabled = True>>%filename%
echo private_repo = True>>%filename%
echo username = >>%filename%
echo password = >>%filename%
