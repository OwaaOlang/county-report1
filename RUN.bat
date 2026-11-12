@echo off
echo Installing what is needed... please wait
pip install -r requirements.txt
echo.
echo Starting report...
python county_report.py
echo.
echo Press any key to close...
pause >nul
