@echo off
setlocal

:: Script para iniciar el monitor automático de archivos Word
title Monitor Word - HTML

echo ========================================
echo    INICIANDO MONITOR WORD - HTML
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no esta instalado
    pause
    exit /b 1
)

:: Instalar dependencias si no están presentes
echo Verificando dependencias...
python -c "import watchdog, mammoth, bs4" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias necesarias...
    pip install watchdog mammoth beautifulsoup4
    if errorlevel 1 (
        echo Error al instalar dependencias
        pause
        exit /b 1
    )
    echo Dependencias instaladas
    echo.
)

:: Iniciar monitor
echo Iniciando monitor automatico...
echo.
python "%~dp0auto_word_watcher.py"

echo.
echo Monitor detenido.
pause