@echo off
cd /d "%~dp0"
echo Installing dependencies...
pip install -r requirements.txt
echo Starting Dota Coach...
python main.py
pause
