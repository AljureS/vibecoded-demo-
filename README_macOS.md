# Monitor Word → HTML para macOS

Sistema automático de conversión de archivos Word (.docx) a HTML con copia al portapapeles.

## 🚀 Instalación Rápida

### 1. Instalar dependencias (solo la primera vez)

Abre Terminal en esta carpeta y ejecuta:

```bash
./instalar_dependencias.sh
```

O manualmente:

```bash
pip3 install watchdog mammoth beautifulsoup4
```

## 📱 Formas de Ejecutar

### Opción 1: Aplicación Nativa (Recomendado)

**Doble clic en:** `Monitor Word HTML.app`

- Se abre Terminal automáticamente
- Inicia el monitor
- Funciona como cualquier aplicación de macOS

**💡 Tip:** Puedes arrastrar `Monitor Word HTML.app` a tu **Dock** o **Escritorio** para acceso rápido

### Opción 2: Script desde Terminal

```bash
./iniciar_monitor.sh
```

### Opción 3: Directamente con Python

```bash
python3 auto_word_watcher.py
```

## 🎯 Cómo Funciona

1. **Ejecuta** la aplicación o script
2. **Arrastra** o **guarda** un archivo .docx en esta carpeta
3. **Automáticamente**:
   - Se convierte a HTML
   - Se copia al portapapeles
   - El archivo .docx original se **elimina**

## 📋 Conversión Manual

Para convertir un archivo específico sin monitor automático:

```bash
python3 word_to_html.py archivo.docx
```

**Conservar el archivo original:**

```bash
python3 word_to_html.py archivo.docx --keep-original
```

**Convertir todos los .docx de una carpeta:**

```bash
python3 word_to_html.py -d carpeta/
```

## 🔧 Verificar Instalación

```bash
python3 --version          # Debe mostrar Python 3.x
pip3 list | grep watchdog  # Debe aparecer watchdog
pip3 list | grep mammoth   # Debe aparecer mammoth
```

## ⚡️ Inicio Automático al Encender Mac (Opcional)

### Método 1: Elementos de Inicio de Sesión (Simple)

1. Ve a **Preferencias del Sistema** → **Usuarios y Grupos**
2. Selecciona tu usuario
3. Ve a la pestaña **Elementos de Inicio**
4. Haz clic en el botón **+**
5. Navega y selecciona `Monitor Word HTML.app`
6. Haz clic en **Agregar**

Ahora se iniciará automáticamente al encender tu Mac.

### Método 2: LaunchAgent (Avanzado)

Crea el archivo: `~/Library/LaunchAgents/com.vibecoded.word2html.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vibecoded.word2html</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/saidaljure/Documents/vibecoded-demo-/auto_word_watcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/Users/saidaljure/Documents/vibecoded-demo-</string>
</dict>
</plist>
```

Luego carga el servicio:

```bash
launchctl load ~/Library/LaunchAgents/com.vibecoded.word2html.plist
```

## 🛠 Solución de Problemas

### "Permission Denied" al ejecutar scripts

```bash
chmod +x instalar_dependencias.sh
chmod +x iniciar_monitor.sh
```

### La aplicación .app no abre

1. Clic derecho → **Abrir**
2. Confirma "Abrir" en el diálogo de seguridad
3. macOS recordará tu elección

### Dependencias no se instalan

```bash
# Verificar pip3
python3 -m pip --version

# Instalar pip si falta
python3 -m ensurepip --upgrade

# Instalar dependencias manualmente
python3 -m pip install watchdog mammoth beautifulsoup4
```

## 📦 Archivos Creados (VmacOS branch)

- `instalar_dependencias.sh` - Script de instalación de dependencias
- `iniciar_monitor.sh` - Script de inicio del monitor
- `Monitor Word HTML.app` - Aplicación nativa de macOS
- `README_macOS.md` - Este archivo

**Los archivos Python originales NO fueron modificados** - funcionan igual en Windows y macOS.

## 🎨 Características

✅ Monitoreo automático de carpeta
✅ Conversión Word → HTML con estilos CSS
✅ Copia automática al portapapeles (pbcopy)
✅ Eliminación automática de archivos .docx procesados
✅ Soporte completo UTF-8 (ñ, tildes, etc.)
✅ Aplicación nativa .app para macOS
✅ Scripts bash ejecutables

## 📝 Notas

- El código Python original **NO fue modificado** - ya era compatible con macOS
- La línea 388-394 de `word_to_html.py` usa `pbcopy` para macOS
- Los scripts .bat y .ps1 de Windows siguen funcionando en esa plataforma
- Esta rama (`VmacOS`) solo agrega soporte de ejecución para macOS
