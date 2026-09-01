@echo off
title Portal de Atencion al Cliente - Iniciador
echo ============================================
echo   Portal de Atencion al Cliente con IA
echo ============================================
echo.
echo Abriendo Backend (puerto 8000) y Frontend (puerto 5173)...
echo Se abren dos ventanas: no las cierres mientras trabajes.
echo Cuando termines, cierralas o pulsa Ctrl+C en cada una.
echo.

start "Backend - Puerto 8000" cmd /k "cd /d %~dp0backend && .venv\Scripts\uvicorn.exe app.main:app --reload"
timeout /t 3 /nobreak >nul
start "Frontend - Puerto 5173" cmd /k "cd /d %~dp0 && pnpm dev"
timeout /t 6 /nobreak >nul
start http://localhost:5173

echo.
echo Listo. El navegador se abre en http://localhost:5173
echo (esta ventana puedes cerrarla; deja abiertas las otras dos)
pause
