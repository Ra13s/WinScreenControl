@echo off
setlocal

:: This script sets the monitor brightness and contrast to 40%.
:: It is part of the WinScreenControl project.
:: It requires Python and the monitorcontrol library to be installed.

:: Find the directory where this script is located.
set "SCRIPT_DIR=%~dp0"

:: Check for python and py launcher
set "PY_CMD=python"
where %PY_CMD% >nul 2>&1 || set "PY_CMD=py"

:: Call the python script to set the brightness and contrast.
"%PY_CMD%" "%SCRIPT_DIR%monitor_control.py" preset set-40 %1

endlocal
