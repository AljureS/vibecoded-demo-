#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertidor Word a HTML optimizado
- Solo genera <div class='container'> sin archivos HTML
- Copia únicamente al portapapeles del sistema
- Elimina archivo Word original tras copia exitosa
- Soporte completo UTF-8 para caracteres especiales (ñ, tildes, etc.)
- Multiplataforma: Windows, macOS, Linux

Uso:
    python word_to_html.py archivo.docx                    # Copia + elimina original
    python word_to_html.py archivo.docx --keep-original    # Copia + conserva original
    python word_to_html.py -d carpeta/                     # Procesa directorio
"""

import os
import sys
import argparse
import subprocess
import traceback
import locale
import time
from pathlib import Path

# Configurar encoding UTF-8 para evitar errores Unicode en Windows
def setup_console_encoding():
    """
    Configura la consola para UTF-8 en Windows y otros sistemas con validación
    """
    try:
        # Intentar configurar UTF-8 como encoding por defecto
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        
        # Configurar variable de entorno para Python
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # Para Windows, intentar configurar página de código UTF-8
        if sys.platform.startswith('win'):
            try:
                # Intentar configurar código de página UTF-8 en Windows
                import subprocess
                subprocess.run(['chcp', '65001'], capture_output=True, shell=True)
            except Exception:
                pass
            
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_ALL, 'Spanish_Spain.UTF-8')
                except locale.Error:
                    pass  # Mantener configuración por defecto
        
        # Validar que el encoding está funcionando
        test_chars = 'ñáéíóúü¿¡'
        try:
            test_encoded = test_chars.encode('utf-8')
            test_decoded = test_encoded.decode('utf-8')
            if test_decoded == test_chars:
                print(f"✅ Configuración UTF-8 exitosa: {test_chars}")
            else:
                print(f"⚠️ Problemas en configuración UTF-8")
        except UnicodeError:
            print(f"❌ Error crítico en configuración UTF-8")
    except Exception as e:
        print(f"⚠️ Error en configuración de encoding: {e}")

def test_unicode_support():
    """
    Prueba si la consola soporta caracteres Unicode
    """
    try:
        # Intentar imprimir un carácter Unicode simple
        test_char = "✓"
        sys.stdout.write(test_char)
        sys.stdout.flush()
        return True
    except (UnicodeEncodeError, UnicodeError):
        return False
    except Exception:
        return False

def safe_print(unicode_text, ascii_fallback=None):
    """
    Imprime texto Unicode de forma segura con fallback ASCII
    
    Args:
        unicode_text (str): Texto con caracteres Unicode/emoji
        ascii_fallback (str): Texto ASCII alternativo
    """
    if ascii_fallback is None:
        # Generar fallback automático reemplazando caracteres comunes
        ascii_fallback = (unicode_text
                         .replace("🚀", "[>]")
                         .replace("→", "->")
                         .replace("✅", "[OK]")
                         .replace("❌", "[X]")
                         .replace("⚠️", "[!]")
                         .replace("🔄", "[~]")
                         .replace("📄", "[DOC]")
                         .replace("📁", "[DIR]")
                         .replace("🗑️", "[DEL]")
                         .replace("💡", "[i]")
                         .replace("🎯", "[*]")
                         .replace("🔧", "[T]")
                         .replace("💾", "[SAVE]")
                         .replace("📏", "[SIZE]")
                         .replace("📂", "[FOLDER]")
                         .replace("🎉", "[SUCCESS]"))
    
    try:
        print(unicode_text)
    except (UnicodeEncodeError, UnicodeError):
        try:
            print(ascii_fallback)
        except Exception:
            # Último recurso: imprimir versión muy simplificada
            print(ascii_fallback.encode('ascii', errors='ignore').decode('ascii'))

# Configurar encoding al importar el módulo
setup_console_encoding()

try:
    import mammoth
    from bs4 import BeautifulSoup
except ImportError:
    safe_print("❌ Dependencias faltantes. Instalando...", "[X] Dependencias faltantes. Instalando...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mammoth', 'beautifulsoup4'])
    import mammoth
    from bs4 import BeautifulSoup

# CSS minimalista y responsive para integración perfecta en sitios web
DEFAULT_CSS_FOR_CONTAINER = """
.container {
    width: 100%;
    padding: 10px;
    margin: 0;
    font-family: inherit;
    line-height: 1.4;
    color: inherit;
}

.container h1 {
    font-size: 1.8em;
    margin: 15px 0 12px 0;
    color: #1a1a1a;
    font-weight: 600;
}

.container h2 {
    font-size: 1.5em;
    margin: 12px 0 8px 0;
    color: #2a2a2a;
    font-weight: 500;
}

.container h3 {
    font-size: 1.2em;
    margin: 10px 0 6px 0;
    color: #3a3a3a;
    font-weight: 500;
}

.container p {
    margin: 0 0 10px 0;
    text-align: left;
    font-size: 1em;
}

.container strong {
    font-weight: 600;
    color: inherit;
}

.container em {
    font-style: italic;
    color: inherit;
}

.container ul, .container ol {
    margin: 8px 0 10px 0;
    padding-left: 20px;
}

.container li {
    margin-bottom: 4px;
    font-size: 1em;
}

.container table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 0.95em;
}

.container th, .container td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    vertical-align: top;
}

.container th {
    background-color: #f5f5f5;
    font-weight: 600;
    color: #333;
}

.container tr:nth-child(even) {
    background-color: #fafafa;
}

.container blockquote {
    margin: 10px 0;
    padding: 8px 15px;
    border-left: 3px solid #ccc;
    background-color: #f9f9f9;
    font-style: italic;
}

/* Asegurar que nada se desborde */
.container * {
    max-width: 100%;
    box-sizing: border-box;
}

.container img {
    max-width: 100%;
    height: auto;
}
"""

def test_clipboard_basic():
    """
    Prueba básica del portapapeles con texto simple
    """
    test_text = "TEST_CLIPBOARD_OK"
    safe_print("🔧 DEBUG: Probando portapapeles básico...")
    
    try:
        if sys.platform.startswith('win'):
            safe_print("🔧 DEBUG: Usando clip.exe para Windows...")
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
            stdout, stderr = process.communicate(input=test_text, timeout=5)
            safe_print(f"🔧 DEBUG: clip.exe returncode: {process.returncode}")
            if stderr:
                safe_print(f"🔧 DEBUG: clip.exe stderr: {stderr}")
            return process.returncode == 0
        else:
            safe_print(f"🔧 DEBUG: Plataforma {sys.platform} - no implementado en test básico")
            return True
    except subprocess.TimeoutExpired:
        safe_print("❌ DEBUG: Timeout en test de portapapeles")
        return False
    except Exception as e:
        safe_print(f"❌ DEBUG: Error en test básico: {str(e)}")
        return False

def copy_to_clipboard(text):
    """
    Copia texto al portapapeles del sistema con logging detallado
    Soporte multiplataforma: Windows, macOS, Linux
    """
    safe_print("🔧 DEBUG: Iniciando copia al portapapeles...")
    safe_print(f"🔧 DEBUG: Plataforma detectada: {sys.platform}")
    safe_print(f"🔧 DEBUG: Tamaño del texto: {len(text)} caracteres")
    
    # Verificar que el texto no esté vacío
    if not text or not text.strip():
        safe_print("❌ DEBUG: Texto vacío o solo espacios")
        return False
    
    # Mostrar una muestra del inicio del texto para debugging
    sample = text[:200].replace('\n', '\\n').replace('\r', '\\r')
    safe_print(f"🔧 DEBUG: Muestra del texto: {sample}...")
    
    try:
        if sys.platform.startswith('win'):
            safe_print("🔧 DEBUG: Usando clip.exe para Windows...")
            
            # CHECKPOINT CRÍTICO: Validar texto antes de enviar a subprocess
            test_words = ['más', 'Bogotá', 'música', 'auténtico', 'ícono']
            corrupted_detected_in_subprocess = False
            
            for word in test_words:
                if word in text:
                    safe_print(f"✅ PRE-SUBPROCESS: '{word}' - CORRECTO")
                else:
                    corrupted_patterns = {'más': 'm├ís', 'Bogotá': 'Bogot├í', 'música': 'm├║sica', 'auténtico': 'aut├®ntico', 'ícono': '├¡cono'}
                    corrupted_form = corrupted_patterns.get(word)
                    if corrupted_form and corrupted_form in text:
                        safe_print(f"❌ PRE-SUBPROCESS: '{word}' → '{corrupted_form}' - CORRUPTO!")
                        corrupted_detected_in_subprocess = True
            
            # Método mejorado para Windows con manejo UTF-8 estricto
            try:
                safe_print("🔧 DEBUG: Creando proceso clip.exe con UTF-8 estricto...")
                
                # Forzar encoding UTF-8 en Windows
                startupinfo = None
                if hasattr(subprocess, 'STARTUPINFO'):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                process = subprocess.Popen(
                    ['clip'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True, 
                    encoding='utf-8',
                    errors='strict',  # Fallar rápido si hay problemas de encoding
                    shell=False,
                    startupinfo=startupinfo
                )
                safe_print(f"🔧 DEBUG: Proceso clip.exe creado, PID: {process.pid}")
                
                # Validar que vamos a enviar texto UTF-8 válido
                try:
                    # Test de encoding antes de enviar
                    test_encoded = text.encode('utf-8', errors='strict')
                    test_decoded = test_encoded.decode('utf-8', errors='strict')
                    if test_decoded == text:
                        safe_print("✅ DEBUG: Texto pasa validación UTF-8 estricta")
                    else:
                        safe_print("❌ DEBUG: Texto falla validación roundtrip UTF-8")
                        return False
                except UnicodeError as encoding_error:
                    safe_print(f"❌ DEBUG: Error de encoding en texto: {encoding_error}")
                    return False
                
                safe_print("🔧 DEBUG: Enviando datos UTF-8 validados al proceso...")
                try:
                    stdout, stderr = process.communicate(input=text, timeout=15)
                    safe_print(f"🔧 DEBUG: clip.exe terminado, returncode: {process.returncode}")
                    
                    if process.returncode == 0:
                        safe_print("✅ DEBUG: clip.exe exitoso con UTF-8 estricto")
                        
                        # CHECKPOINT 4: Intentar verificar lo que se copió (si es posible)
                        safe_print("🔍 CHECKPOINT 4: Verificación post-clipboard")
                        return True
                    else:
                        safe_print(f"❌ DEBUG: clip.exe falló con código: {process.returncode}")
                        if stderr:
                            safe_print(f"❌ DEBUG: stderr: {stderr}")
                        return False
                        
                except subprocess.TimeoutExpired:
                    safe_print("❌ DEBUG: Timeout en clip.exe - matando proceso")
                    try:
                        process.kill()
                        process.wait(timeout=5)
                    except:
                        pass
                    return False
                    
            except Exception as win_error:
                safe_print(f"❌ DEBUG: Error creando proceso clip.exe: {win_error}")
                
                # Fallback: intentar con método alternativo
                safe_print("🔄 DEBUG: Intentando método alternativo de clipboard...")
                try:
                    # Método alternativo usando echo y pipe
                    alt_process = subprocess.run(
                        f'echo {text} | clip', 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        encoding='utf-8',
                        timeout=10
                    )
                    if alt_process.returncode == 0:
                        safe_print("✅ DEBUG: Método alternativo exitoso")
                        return True
                    else:
                        safe_print(f"❌ DEBUG: Método alternativo falló: {alt_process.stderr}")
                        return False
                except Exception as alt_error:
                    safe_print(f"❌ DEBUG: Método alternativo también falló: {alt_error}")
                    return False
                
        elif sys.platform.startswith('darwin'):
            safe_print("🔧 DEBUG: Usando pbcopy para macOS...")
            # macOS - pbcopy
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
            stdout, stderr = process.communicate(input=text, timeout=10)
            safe_print(f"🔧 DEBUG: pbcopy returncode: {process.returncode}")
            return process.returncode == 0
            
        elif sys.platform.startswith('linux'):
            safe_print("🔧 DEBUG: Probando xclip para Linux...")
            # Linux - xclip o xsel
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                         stdin=subprocess.PIPE, text=True, encoding='utf-8')
                stdout, stderr = process.communicate(input=text, timeout=10)
                safe_print(f"🔧 DEBUG: xclip returncode: {process.returncode}")
                return process.returncode == 0
            except FileNotFoundError:
                safe_print("🔧 DEBUG: xclip no encontrado, probando xsel...")
                try:
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'], 
                                             stdin=subprocess.PIPE, text=True, encoding='utf-8')
                    stdout, stderr = process.communicate(input=text, timeout=10)
                    safe_print(f"🔧 DEBUG: xsel returncode: {process.returncode}")
                    return process.returncode == 0
                except FileNotFoundError:
                    safe_print("❌ Error: Instala xclip o xsel para soporte de portapapeles en Linux")
                    return False
        else:
            safe_print(f"❌ Plataforma no soportada: {sys.platform}")
            return False
            
    except subprocess.TimeoutExpired:
        safe_print("❌ DEBUG: Timeout general en copia al portapapeles")
        return False
    except Exception as e:
        safe_print(f"❌ ERROR DEBUG: Excepción en copy_to_clipboard: {str(e)}")
        safe_print(f"❌ DEBUG: Tipo de excepción: {type(e).__name__}")
        traceback.print_exc()
        return False

def safe_delete_file(file_path):
    """
    Elimina archivo de forma segura con manejo de errores y reintentos
    """
    import shutil
    import tempfile
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Verificar que el archivo existe antes de intentar eliminarlo
            if not os.path.exists(file_path):
                safe_print(f"🔧 DEBUG: Archivo ya no existe: {file_path}")
                return True
            
            # Intentar eliminar el archivo
            os.remove(file_path)
            safe_print(f"🔧 DEBUG: Archivo eliminado exitosamente: {os.path.basename(file_path)}")
            return True
            
        except PermissionError:
            safe_print(f"🔧 DEBUG: Intento {attempt + 1}/{max_retries} - Acceso denegado a {os.path.basename(file_path)}")
            if attempt < max_retries - 1:
                # Esperar un momento y reintentar
                time.sleep(2)
                continue
            else:
                # Último intento: mover a carpeta temporal
                try:
                    temp_dir = tempfile.gettempdir()
                    temp_name = f"temp_docx_{int(time.time())}_{os.path.basename(file_path)}"
                    temp_path = os.path.join(temp_dir, temp_name)
                    
                    shutil.move(file_path, temp_path)
                    safe_print(f"📁 Archivo movido a temporal: {temp_name}")
                    safe_print(f"⚠️  No se pudo eliminar, pero se movió fuera del directorio de trabajo")
                    return True
                    
                except Exception as move_error:
                    safe_print(f"❌ No se pudo eliminar ni mover: {str(move_error)}")
                    return False
                    
        except OSError as e:
            safe_print(f"🔧 DEBUG: Error OSError intento {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            else:
                safe_print(f"⚠️  No se pudo eliminar después de {max_retries} intentos: {str(e)}")
                return False
    
    return False

def convert_docx_to_html_div(docx_path, custom_css=None, keep_original=False):
    """
    Convierte archivo .docx a HTML div y lo copia al portapapeles
    
    Args:
        docx_path (str): Ruta del archivo .docx
        custom_css (str): CSS personalizado opcional
        keep_original (bool): Si mantener el archivo original
    
    Returns:
        bool: True si la conversión fue exitosa
    """
    docx_path = Path(docx_path)
    
    safe_print(f"🔧 DEBUG: Iniciando conversión de {docx_path}")
    
    if not docx_path.exists():
        safe_print(f"❌ Error: {docx_path} no existe")
        return False
    
    if not docx_path.suffix.lower() == '.docx':
        safe_print(f"❌ Error: {docx_path} no es un archivo .docx")
        return False
    
    safe_print(f"🔄 Procesando: {docx_path.name}")
    
    # Primero probar portapapeles básico
    safe_print("🔧 DEBUG: Probando funcionalidad básica de portapapeles...")
    if not test_clipboard_basic():
        safe_print("❌ ERROR: Portapapeles básico no funciona")
        return False
    safe_print("✅ DEBUG: Portapapeles básico funciona")
    
    try:
        safe_print("🔧 DEBUG: Abriendo archivo docx...")
        # Convertir Word a HTML usando mammoth con configuración avanzada
        with open(docx_path, "rb") as docx_file:
            safe_print("🔧 DEBUG: Llamando mammoth.convert_to_html()...")
            
            # Configuración avanzada de mammoth para mejor conversión
            try:
                # Mapeo de estilos para mejor estructura semántica
                style_map = """
                p[style-name='Heading 1'] => h1:fresh
                p[style-name='Heading 2'] => h2:fresh
                p[style-name='Heading 3'] => h3:fresh
                p[style-name='Title'] => h1:fresh
                p[style-name='Subtitle'] => h2:fresh
                """
                
                mammoth_options = {
                    "style_map": style_map,
                    "include_embedded_style_map": False,
                    "include_default_style_map": True,
                }
                
                # Intentar con imágenes si está disponible
                if hasattr(mammoth, 'images'):
                    mammoth_options["convert_image"] = mammoth.images.data_uri
                
                safe_print("🔧 DEBUG: Usando configuración avanzada de mammoth...")
                result = mammoth.convert_to_html(docx_file, **mammoth_options)
                
            except (TypeError, AttributeError) as e:
                safe_print(f"🔧 DEBUG: Fallback a configuración básica: {str(e)}")
                # Fallback a configuración básica
                result = mammoth.convert_to_html(docx_file)
            
            html_content = result.value
            messages = result.messages
            safe_print(f"🔧 DEBUG: Mammoth completado, {len(html_content)} caracteres HTML generados")
            
            # CHECKPOINT 1: Validación inmediata POST-MAMMOTH
            safe_print("🔍 CHECKPOINT 1: Validación POST-MAMMOTH")
            test_words = ['más', 'Bogotá', 'música', 'auténtico', 'ícono', 'recibirá', 'generación', 'próximo']
            corruption_detected = False
            
            for word in test_words:
                if word in html_content:
                    safe_print(f"✅ CHECKPOINT 1: '{word}' - CORRECTO")
                else:
                    # Buscar versiones corruptas
                    corrupted_patterns = {
                        'más': 'm├ís',
                        'Bogotá': 'Bogot├í', 
                        'música': 'm├║sica',
                        'auténtico': 'aut├®ntico',
                        'ícono': '├¡cono',
                        'recibirá': 'recibir├í',
                        'generación': 'generaci├│n',
                        'próximo': 'pr├│ximo'
                    }
                    
                    corrupted_form = corrupted_patterns.get(word)
                    if corrupted_form and corrupted_form in html_content:
                        safe_print(f"❌ CHECKPOINT 1: '{word}' → '{corrupted_form}' - CORRUPTO EN MAMMOTH!")
                        corruption_detected = True
                    else:
                        safe_print(f"⚠️  CHECKPOINT 1: '{word}' - NO ENCONTRADO")
            
            # Mostrar muestra del contenido mammoth para debugging
            sample_content = html_content[:200].replace('\n', ' ').replace('\r', '')
            safe_print(f"🔍 MUESTRA POST-MAMMOTH: {sample_content}...")
            
            if corruption_detected:
                safe_print("🚨 CRÍTICO: Corrupción detectada en la salida de mammoth")
                safe_print("🔧 Intentando with different mammoth approach...")
                
                # Intento de corrección inmediata
                try:
                    # Re-abrir archivo con encoding específico
                    with open(docx_path, "rb") as fresh_docx:
                        result_retry = mammoth.convert_to_html(fresh_docx)
                        html_content = result_retry.value
                        safe_print("🔄 Reintentando conversión mammoth...")
                        
                        # Re-validar
                        if 'más' in html_content and 'm├ís' not in html_content:
                            safe_print("✅ Corrección mammoth exitosa")
                        else:
                            safe_print("❌ Corrección mammoth fallida - problema más profundo")
                except Exception as retry_error:
                    safe_print(f"❌ Error en reintento mammoth: {retry_error}")
            
            # Verificar caracteres especiales generales
            special_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', '¿', '¡', 'ü', 'Ñ', 'Á', 'É', 'Í', 'Ó', 'Ú']
            found_special = [char for char in special_chars if char in html_content]
            if found_special:
                safe_print(f"🔧 DEBUG: Caracteres especiales detectados: {', '.join(found_special)}")
        
        safe_print("🔧 DEBUG: Procesando HTML con BeautifulSoup...")
        # Procesar HTML con BeautifulSoup para mejor formato
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Optimización y limpieza del HTML
        safe_print("🔧 DEBUG: Iniciando limpieza de HTML...")
        
        # 1. Eliminar párrafos completamente vacíos
        empty_paragraphs = soup.find_all('p', string=lambda text: not text or not text.strip())
        for p in empty_paragraphs:
            p.decompose()
        
        # 2. Limpiar atributos de estilo inline que pueden causar conflictos
        for element in soup.find_all(attrs={"style": True}):
            del element['style']
            
        # 3. Limpiar atributos class innecesarios de mammoth
        for element in soup.find_all(attrs={"class": True}):
            classes = element.get('class', [])
            # Mantener solo clases que no sean de mammoth
            clean_classes = [cls for cls in classes if not cls.startswith('MsoNormal') and not cls.startswith('mso')]
            if clean_classes:
                element['class'] = clean_classes
            else:
                del element['class']
        
        # 4. Convertir divs innecesarios a párrafos semánticamente correctos
        for div in soup.find_all('div'):
            # Si el div solo contiene texto, convertirlo a párrafo
            if div.string and not div.find_all():
                new_p = soup.new_tag('p')
                new_p.string = div.string
                div.replace_with(new_p)
        
        # 5. Limpiar espacios en blanco excesivos
        for element in soup.find_all(string=True):
            if element.parent.name not in ['script', 'style']:
                cleaned = ' '.join(element.split())
                if cleaned != element:
                    element.replace_with(cleaned)
        
        # 6. Asegurar estructura semántica de headings
        headings_fixed = 0
        for tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(tag_name):
                # Limpiar headings vacíos
                if not heading.get_text(strip=True):
                    heading.decompose()
                    headings_fixed += 1
        
        safe_print(f"🔧 DEBUG: Limpieza completada - {headings_fixed} elementos optimizados")
        
        # CHECKPOINT 2: Validación POST-BEAUTIFULSOUP
        safe_print("🔍 CHECKPOINT 2: Validación POST-BEAUTIFULSOUP")
        soup_text = soup.get_text()
        
        test_words = ['más', 'Bogotá', 'música', 'auténtico', 'ícono', 'recibirá', 'generación', 'próximo']
        soup_corruption_detected = False
        
        for word in test_words:
            if word in soup_text:
                safe_print(f"✅ CHECKPOINT 2: '{word}' - CORRECTO")
            else:
                corrupted_patterns = {
                    'más': 'm├ís', 'Bogotá': 'Bogot├í', 'música': 'm├║sica',
                    'auténtico': 'aut├®ntico', 'ícono': '├¡cono', 'recibirá': 'recibir├í',
                    'generación': 'generaci├│n', 'próximo': 'pr├│ximo'
                }
                
                corrupted_form = corrupted_patterns.get(word)
                if corrupted_form and corrupted_form in soup_text:
                    safe_print(f"❌ CHECKPOINT 2: '{word}' → '{corrupted_form}' - CORRUPTO EN BEAUTIFULSOUP!")
                    soup_corruption_detected = True
                else:
                    safe_print(f"⚠️  CHECKPOINT 2: '{word}' - NO ENCONTRADO")
        
        # Mostrar muestra del contenido soup para debugging
        sample_soup = soup_text[:200].replace('\n', ' ').replace('\r', '')
        safe_print(f"🔍 MUESTRA POST-BEAUTIFULSOUP: {sample_soup}...")
        
        if soup_corruption_detected:
            safe_print("🚨 CRÍTICO: BeautifulSoup introdujo corrupción de encoding")
        
        safe_print("🔧 DEBUG: BeautifulSoup procesamiento completado")
        
        safe_print("🔧 DEBUG: Generando div container...")
        
        # Determinar qué CSS usar
        css_to_use = custom_css if custom_css else DEFAULT_CSS_FOR_CONTAINER
        
        # Generar div container con CSS incluido internamente
        container_html = f'''<div class="container">
<style>
{css_to_use}
</style>
{soup.prettify()}
</div>'''
        
        safe_print("🔧 DEBUG: Validando encoding UTF-8 en todo el proceso...")
        
        # Validación de encoding paso a paso
        def validate_encoding_step(content, step_name):
            test_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', '¿', '¡', 'ü', 'Ñ', 'Á', 'É', 'Í', 'Ó', 'Ú']
            found = [char for char in test_chars if char in content]
            if found:
                safe_print(f"🔧 DEBUG: {step_name} - Caracteres especiales OK: {', '.join(found[:3])}{'...' if len(found) > 3 else ''}")
            return len(found)
        
        # Validar encoding en BeautifulSoup output
        soup_html = str(soup)
        chars_in_soup = validate_encoding_step(soup_html, "Post-BeautifulSoup")
        
        # Validar encoding en container HTML final
        chars_in_container = validate_encoding_step(container_html, "Container HTML")
        
        # Verificar que no perdimos caracteres en el proceso
        if chars_in_soup > 0 and chars_in_container == 0:
            safe_print("⚠️  WARNING: Se perdieron caracteres especiales en la generación del container")
            # Regenerar container preservando mejor el encoding
            container_html = f'''<div class="container">
<style>
{css_to_use}
</style>
{soup_html}
</div>'''
            chars_in_container = validate_encoding_step(container_html, "Container HTML (regenerado)")
        
        # Validación final de string UTF-8
        if isinstance(container_html, str):
            safe_print("🔧 DEBUG: HTML es string nativo UTF-8 ✓")
            try:
                # Test de roundtrip encoding para verificar integridad
                test_encoded = container_html.encode('utf-8')
                test_decoded = test_encoded.decode('utf-8')
                if test_decoded == container_html:
                    safe_print("🔧 DEBUG: Validación roundtrip UTF-8 exitosa ✓")
                else:
                    safe_print("⚠️  WARNING: Problemas en roundtrip UTF-8")
            except UnicodeError as e:
                safe_print(f"⚠️  WARNING: Error en validación UTF-8: {e}")
        else:
            container_html = str(container_html)
            safe_print("🔧 DEBUG: Convertido a string UTF-8")
            
        safe_print(f"🔧 DEBUG: HTML final tiene {len(container_html)} caracteres")
        safe_print("🔧 DEBUG: CSS responsive incluido en el contenedor")
        safe_print(f"🔧 DEBUG: Caracteres especiales preservados: {chars_in_container} tipos")
        
        # CHECKPOINT 3: Validación PRE-CLIPBOARD
        safe_print("🔍 CHECKPOINT 3: Validación PRE-CLIPBOARD")
        test_words = ['más', 'Bogotá', 'música', 'auténtico', 'ícono', 'recibirá', 'generación', 'próximo']
        clipboard_corruption_detected = False
        
        for word in test_words:
            if word in container_html:
                safe_print(f"✅ CHECKPOINT 3: '{word}' - CORRECTO")
            else:
                corrupted_patterns = {
                    'más': 'm├ís', 'Bogotá': 'Bogot├í', 'música': 'm├║sica',
                    'auténtico': 'aut├®ntico', 'ícono': '├¡cono', 'recibirá': 'recibir├í',
                    'generación': 'generaci├│n', 'próximo': 'pr├│ximo'
                }
                
                corrupted_form = corrupted_patterns.get(word)
                if corrupted_form and corrupted_form in container_html:
                    safe_print(f"❌ CHECKPOINT 3: '{word}' → '{corrupted_form}' - CORRUPTO EN CONTAINER!")
                    clipboard_corruption_detected = True
                else:
                    safe_print(f"⚠️  CHECKPOINT 3: '{word}' - NO ENCONTRADO")
        
        # Mostrar muestra del container HTML para debugging
        sample_container = container_html[:300].replace('\n', ' ')
        safe_print(f"🔍 MUESTRA PRE-CLIPBOARD: {sample_container}...")
        
        if clipboard_corruption_detected:
            safe_print("🚨 CRÍTICO: Corrupción en container HTML antes del portapapeles")
            
            # Intento de corrección de corrupción
            safe_print("🔧 Intentando corrección de corrupción...")
            correction_map = {
                'm├ís': 'más', 'Bogot├í': 'Bogotá', 'm├║sica': 'música',
                'aut├®ntico': 'auténtico', '├¡cono': 'ícono', 'recibir├í': 'recibirá',
                'generaci├│n': 'generación', 'pr├│ximo': 'próximo'
            }
            
            corrected_html = container_html
            corrections_made = 0
            for corrupted, correct in correction_map.items():
                if corrupted in corrected_html:
                    corrected_html = corrected_html.replace(corrupted, correct)
                    corrections_made += 1
                    safe_print(f"🔧 Corregido: '{corrupted}' → '{correct}'")
            
            if corrections_made > 0:
                container_html = corrected_html
                safe_print(f"✅ Aplicadas {corrections_made} correcciones de encoding")
            
        safe_print("🔧 DEBUG: Iniciando copia al portapapeles...")
        # Copiar al portapapeles
        if copy_to_clipboard(container_html):
            safe_print(f"✅ HTML copiado al portapapeles ({len(container_html)} caracteres)")
            safe_print("🎯 Soporte completo para caracteres especiales (ñ, tildes, etc.)")
            
            # Solo eliminar si la copia fue exitosa Y no se pidió conservar
            if not keep_original:
                if safe_delete_file(docx_path):
                    safe_print(f"🗑️  Archivo original eliminado: {docx_path.name}")
                else:
                    safe_print("⚠️  Archivo original conservado por error en eliminación")
            else:
                safe_print(f"📁 Archivo original conservado: {docx_path.name}")
        else:
            safe_print("❌ Error: No se pudo copiar al portapapeles")
            safe_print("🔧 DEBUG: Intentando fallback - guardar como archivo temporal...")
            
            # Fallback: guardar como archivo temporal para debugging
            try:
                temp_html = docx_path.with_suffix('.temp_debug.html')
                with open(temp_html, 'w', encoding='utf-8') as f:
                    f.write(container_html)
                safe_print(f"💾 DEBUG: Contenido guardado temporalmente en: {temp_html}")
                safe_print(f"📏 DEBUG: Tamaño del archivo: {temp_html.stat().st_size} bytes")
            except Exception as fallback_error:
                safe_print(f"❌ DEBUG: También falló el fallback: {fallback_error}")
            
            safe_print(f"📁 Archivo original conservado por seguridad: {docx_path.name}")
            return False
        
        # Mostrar advertencias de conversión si existen
        if messages:
            safe_print("⚠️  Advertencias de conversión:")
            for msg in messages[:3]:  # Limitar a 3 mensajes
                print(f"   • {msg}")
            if len(messages) > 3:
                print(f"   ... y {len(messages) - 3} más")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ Error durante conversión: {str(e)}")
        safe_print(f"📁 Archivo original conservado por seguridad: {docx_path.name}")
        return False

def process_directory(directory_path, custom_css=None, keep_original=False):
    """
    Procesa todos los archivos .docx en un directorio
    """
    directory = Path(directory_path)
    
    if not directory.is_dir():
        safe_print(f"❌ Error: {directory} no es un directorio válido")
        return 0
    
    # Buscar archivos .docx
    docx_files = list(directory.glob('*.docx'))
    docx_files = [f for f in docx_files if not f.name.startswith('~$')]  # Excluir temporales
    
    if not docx_files:
        safe_print(f"❌ No se encontraron archivos .docx en {directory}")
        return 0
    
    safe_print(f"📂 Procesando {len(docx_files)} archivos en {directory}")
    print("=" * 50)
    
    success_count = 0
    for docx_file in docx_files:
        if convert_docx_to_html_div(docx_file, custom_css, keep_original):
            success_count += 1
        print("-" * 30)
    
    safe_print(f"✅ Completado: {success_count}/{len(docx_files)} archivos procesados exitosamente")
    return success_count

def load_custom_css(css_path):
    """
    Carga CSS personalizado desde archivo
    """
    css_path = Path(css_path)
    if not css_path.exists():
        safe_print(f"⚠️  Archivo CSS no encontrado: {css_path}")
        return None
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        safe_print(f"⚠️  Error cargando CSS: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Convertidor Word a HTML optimizado - Solo portapapeles, auto-elimina originales',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s documento.docx                     # Copia a portapapeles + elimina original
  %(prog)s documento.docx --keep-original    # Copia a portapapeles + conserva original
  %(prog)s -d carpeta/                       # Procesa todos los .docx del directorio
  %(prog)s archivo.docx -c estilos.css       # Usa CSS personalizado
        """
    )
    
    parser.add_argument('input', nargs='?', help='Archivo .docx de entrada')
    parser.add_argument('-d', '--dir', help='Procesar directorio completo')
    parser.add_argument('-c', '--css', help='Archivo CSS personalizado')
    parser.add_argument('--keep-original', action='store_true', 
                       help='Conservar archivo original (por defecto se elimina)')
    
    args = parser.parse_args()
    
    if not args.input and not args.dir:
        parser.print_help()
        return 1
    
    # Cargar CSS personalizado si se especifica
    custom_css = None
    if args.css:
        custom_css = load_custom_css(args.css)
    
    safe_print("🚀 CONVERTIDOR WORD → HTML (Solo Portapapeles)")
    print("=" * 50)
    
    success = False
    
    if args.dir:
        # Procesar directorio
        success_count = process_directory(args.dir, custom_css, args.keep_original)
        success = success_count > 0
    elif args.input:
        # Procesar archivo individual
        success = convert_docx_to_html_div(args.input, custom_css, args.keep_original)
    
    print("=" * 50)
    if success:
        safe_print("🎉 ¡Proceso completado exitosamente!")
        if not args.keep_original:
            safe_print("💡 Usa --keep-original para conservar archivos .docx")
    else:
        safe_print("❌ El proceso falló. Revisa los errores arriba.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())