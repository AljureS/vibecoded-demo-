@echo off
setlocal enabledelayedexpansion

:: Script para convertir archivos Word a HTML con estilos
:: Uso: word2html.bat archivo.docx [archivo.html] [estilos.css]

echo ==========================================
echo    CONVERTIDOR WORD → HTML OPTIMIZADO
echo ==========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en PATH
    echo    Instala Python desde https://python.org
    pause
    exit /b 1
)

:: Verificar si mammoth está instalado
python -c "import mammoth" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  mammoth no está instalado. Instalando dependencias...
    pip install mammoth beautifulsoup4
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas correctamente
    echo.
)

:: Verificar argumentos
if "%~1"=="" (
    echo Uso: %~nx0 archivo.docx [--keep-original] [-c estilos.css]
    echo      Por defecto: copia a portapapeles + elimina archivo original
    echo.
    echo Ejemplos:
    echo   %~nx0 documento.docx                           (copia + elimina original)
    echo   %~nx0 documento.docx --keep-original           (copia + conserva original)
    echo   %~nx0 documento.docx -c mis_estilos.css        (con CSS personalizado)
    echo   %~nx0 -d carpeta_con_docx                      (procesa directorio)
    echo   %~nx0 -d carpeta/ --keep-original              (directorio + conservar)
    echo.
    pause
    exit /b 1
)

:: Ejecutar script Python pasando todos los argumentos
echo Ejecutando conversión optimizada...
python "%~dp0word_to_html.py" %*

echo.
if errorlevel 1 (
    echo ❌ La conversión falló
) else (
    echo 🎉 ¡Conversión completada exitosamente!
)

echo.
pause