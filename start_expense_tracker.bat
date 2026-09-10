@echo off
cd /d "%~dp0"

start "" python web_app/app.py

timeout /t 3 /nobreak >nul

start "" http://127.0.0.1:5000