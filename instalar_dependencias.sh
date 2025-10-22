#!/bin/bash
# Script de instalación de dependencias para macOS

echo "==========================================="
echo "  INSTALADOR DE DEPENDENCIAS - macOS"
echo "==========================================="
echo ""

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Instala Python desde: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"
echo ""

# Verificar pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "Instalando pip3..."
    python3 -m ensurepip --upgrade
fi

echo "✅ pip3 encontrado"
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias Python..."
echo ""

pip3 install watchdog mammoth beautifulsoup4

if [ $? -eq 0 ]; then
    echo ""
    echo "==========================================="
    echo "✅ ¡Instalación completada exitosamente!"
    echo "==========================================="
    echo ""
    echo "Dependencias instaladas:"
    echo "  - watchdog (monitor de archivos)"
    echo "  - mammoth (conversión Word)"
    echo "  - beautifulsoup4 (procesamiento HTML)"
    echo ""
else
    echo ""
    echo "❌ Error durante la instalación"
    echo "Intenta manualmente: pip3 install watchdog mammoth beautifulsoup4"
    exit 1
fi
