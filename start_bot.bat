@echo off
cd /d "%~dp0"
if not exist ".env" (
    echo .env was not found. Launching setup_env.bat...
    call setup_env.bat
    if not exist ".env" (
        echo .env is still missing. Bot startup is canceled.
        pause
        exit /b 1
    )
)
echo To update settings later, run setup_env.bat.
python MinecraftDiscordBot.py
pause
