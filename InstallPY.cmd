rem Define the Python installer download URL
set PYTHON_URL=https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

rem Define the filename for the downloaded installer
set INSTALLER_FILENAME=python_installer.exe

rem Define the installation directory for Python
set PYTHON_INSTALL_DIR=C:\Python310

rem Download Python installer
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%INSTALLER_FILENAME%')"

rem Install Python silently
echo Installing Python...
%INSTALLER_FILENAME% /quiet InstallAllUsers=1 TargetDir="%PYTHON_INSTALL_DIR%" PrependPath=1

rem Check if installation was successful
if exist "%PYTHON_INSTALL_DIR%\python.exe" (
    echo Python has been successfully installed.
) else (
    echo An error occurred while installing Python.
)

rem Clean up downloaded installer
del %INSTALLER_FILENAME%

rem Exit the script
exit
