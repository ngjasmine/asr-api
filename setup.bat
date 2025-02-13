@echo off
SET VENV_NAME=asr-api

echo 🚀 Setting up Python virtual environment "%VENV_NAME%"...

:: Check if Python is installed (checks both "python" and "python3" for compatibility)
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    where python3 >nul 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Python is not installed. Please install Python 3 and rerun this script.
        exit /b 1
    )
)

:: Create virtual environment if it doesn’t exist
IF NOT EXIST %VENV_NAME% (
    echo 🔹 Creating virtual environment with Python 3...
    python -m venv %VENV_NAME%
) ELSE (
    echo ✅ Virtual environment "%VENV_NAME%" already exists. Skipping creation.
)

:: Activate virtual environment
echo 🔹 Activating virtual environment...
call %VENV_NAME%\Scripts\activate

:: Upgrade pip
echo 🔹 Upgrading pip...
python -m pip install --upgrade pip

:: Check if requirements.txt exists before installing dependencies
IF EXIST requirements.txt (
    echo 🔹 Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo ⚠️ Warning: requirements.txt not found. Skipping dependency installation.
)

echo ✅ Setup complete! To activate the environment, run:
echo    call %VENV_NAME%\Scripts\activate
echo Or, if running manually outside this script, use:
echo    %VENV_NAME%\Scripts\activate.bat