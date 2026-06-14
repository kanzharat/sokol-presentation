@echo off
chcp 65001 >nul
title Редактор презентации Sokol
start "" "http://127.0.0.1:8765/ads/sokol-ads.html"
netstat -ano | findstr "LISTENING" | findstr ":8765" >nul
if %errorlevel%==0 (
  echo Сервер уже запущен — презентация открыта в браузере.
  timeout /t 3 >nul
  exit /b
)
echo Редактор запущен. НЕ ЗАКРЫВАЙТЕ это окно, пока редактируете.
echo Браузер открылся сам. Если нет — откройте http://127.0.0.1:8765
python "%~dp0ads\edit_server.py" 8765
pause
