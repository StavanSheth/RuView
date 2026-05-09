@echo off
title RuView Launcher
echo =======================================================
echo          Starting RuView Sensing Backend
echo =======================================================
echo 1. Ensure your Windows Mobile Hotspot (STAVAN-DESKSTOP 2500) is ON.
echo 2. Ensure both ESP32 boards are plugged into power.
echo.
echo Because you already flashed and provisioned the hardware, 
echo the ESPs will connect automatically to the hotspot and 
echo stream data instantly to 192.168.137.1!
echo =======================================================
echo.

cd /d "%~dp0..\backend\rust-port\wifi-densepose-rs"
set PATH=%PATH%;%USERPROFILE%\.cargo\bin

echo Starting the Rust backend natively...
start "" "cargo" run -p wifi-densepose-sensing-server -- --http-port 3005 --source esp32 --ui-path "%~dp0..\frontend\ui"

echo Waiting 5 seconds for the server to initialize...
timeout /t 5 /nobreak >nul

echo Opening the Dashboard...
start http://localhost:3005/ui/index.html

echo.
echo Complete! The background terminal running cargo must stay open.
echo You can now safely close this launcher window.
pause
