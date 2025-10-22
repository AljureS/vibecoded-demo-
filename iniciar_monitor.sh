#!/bin/bash
# Script de inicio del monitor automático Word to HTML para macOS

# Obtener el directorio donde está el script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Banner con colores
clear

# Colores ANSI
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}SSSSS   AAA   III  DDD   ${NC}"
echo -e "${GREEN}S      A   A   I   D   D  ${NC}"
echo -e "${GREEN}SSSSS  AAAAA   I   D   D  ${NC}"
echo -e "${GREEN}    S  A   A   I   D   D  ${NC}"
echo -e "${GREEN}SSSSS  A   A  III  DDD   ${NC}"
echo ""
echo -e "${YELLOW}EEEEE  SSSSS  TTTTT  U   U  V   V  OOO  ${NC}"
echo -e "${YELLOW}E      S        T    U   U  V   V  O   O${NC}"
echo -e "${YELLOW}EEEEE  SSSSS    T    U   U  V   V  O   O${NC}"
echo -e "${YELLOW}E          S    T    U   U   V V   O   O${NC}"
echo -e "${YELLOW}EEEEE  SSSSS    T     UUU     V    OOO  ${NC}"
echo ""
echo -e "${CYAN} AAA    CCC    AAA   ${NC}"
echo -e "${CYAN}A   A  C      A   A  ${NC}"
echo -e "${CYAN}AAAAA  C      AAAAA  ${NC}"
echo -e "${CYAN}A   A  C      A   A  ${NC}"
echo -e "${CYAN}A   A   CCC   A   A  ${NC}"
echo ""
echo -e "${RED}       MONITOR WORD → HTML       ${NC}"
echo -e "${WHITE}====================================${NC}"
echo ""
echo "Directorio: $SCRIPT_DIR"
echo ""

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    echo "Instala Python desde: https://www.python.org/downloads/"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi

# Verificar dependencias
echo "🔍 Verificando dependencias..."
python3 -c "import watchdog, mammoth, bs4" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Faltan dependencias Python"
    echo ""
    echo "¿Deseas instalarlas automáticamente? (s/n)"
    read -r respuesta

    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        echo ""
        echo "📦 Instalando dependencias..."
        pip3 install watchdog mammoth beautifulsoup4

        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ Error instalando dependencias"
            echo "Intenta manualmente: pip3 install watchdog mammoth beautifulsoup4"
            echo ""
            read -p "Presiona Enter para salir..."
            exit 1
        fi
    else
        echo ""
        echo "❌ No se pueden iniciar sin dependencias"
        echo "Ejecuta primero: ./instalar_dependencias.sh"
        echo ""
        read -p "Presiona Enter para salir..."
        exit 1
    fi
fi

echo "✅ Dependencias verificadas"
echo ""

# Cambiar al directorio del script
cd "$SCRIPT_DIR"

# Verificar que existe el script Python
if [ ! -f "auto_word_watcher.py" ]; then
    echo "❌ Error: No se encuentra auto_word_watcher.py"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi

echo "🚀 Iniciando monitor automático..."
echo ""
echo "==========================================="
echo ""

# Ejecutar el monitor
python3 auto_word_watcher.py

# Si el monitor se detiene, esperar antes de cerrar
echo ""
echo "Monitor detenido."
read -p "Presiona Enter para salir..."
