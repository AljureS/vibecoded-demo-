#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script que monitorea automáticamente una carpeta y convierte archivos Word a HTML
cuando se detectan nuevos archivos .docx
Soporte completo para caracteres especiales del español (tildes, ñ, etc.)
Requiere: pip install watchdog mammoth beautifulsoup4
"""

import os
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading
from datetime import datetime

class WordFileHandler(FileSystemEventHandler):
    """Maneja eventos del sistema de archivos para archivos Word"""
    
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.processed_files = set()
        self.conversion_script = os.path.join(script_dir, "word_to_html.py")
        self.processing_queue = []
        self.processing_lock = threading.Lock()
        
        # Debouncing: diccionario para rastrear timers pendientes
        self.pending_timers = {}
        self.timer_lock = threading.Lock()
        
        # Verificar que el script de conversión existe
        if not os.path.exists(self.conversion_script):
            print(f"Error: No se encontro {self.conversion_script}")
            sys.exit(1)
    
    def log_event(self, message):
        """Registra eventos con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def safe_delete_file(self, file_path):
        """Elimina archivo de forma segura con reintentos"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.log_event(f"✅ Archivo eliminado: {os.path.basename(file_path)}")
                    return True
                else:
                    self.log_event(f"⚠️  Archivo ya no existe: {os.path.basename(file_path)}")
                    return True
            except PermissionError:
                self.log_event(f"⚠️  Archivo en uso (intento {attempt + 1}/{max_attempts}): {os.path.basename(file_path)}")
                if attempt < max_attempts - 1:
                    time.sleep(2)  # Esperar antes del siguiente intento
            except Exception as e:
                self.log_event(f"❌ Error eliminando archivo: {str(e)}")
                break
        
        self.log_event(f"❌ No se pudo eliminar después de {max_attempts} intentos: {os.path.basename(file_path)}")
        return False
    
    def is_word_file(self, file_path):
        """Verifica si es un archivo Word válido"""
        return (
            file_path.lower().endswith('.docx') and 
            not file_path.startswith('~$') and  # Archivos temporales de Word
            os.path.exists(file_path) and
            os.path.getsize(file_path) > 0  # No archivos vacíos
        )
    
    def convert_file(self, file_path):
        """Convierte un archivo Word a HTML"""
        try:
            # Esperar un poco para asegurar que el archivo esté completamente escrito
            time.sleep(2)
            
            if not os.path.exists(file_path):
                return
            
            self.log_event(f"Convirtiendo: {os.path.basename(file_path)}")
            
            # Ejecutar script de conversión - eliminar originales después del procesamiento
            cmd = [sys.executable, self.conversion_script, file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.script_dir, encoding='utf-8')
            
            if result.returncode == 0:
                self.log_event(f"Conversión exitosa - HTML copiado al portapapeles")
                self.log_event(f"✅ Soporte completo para caracteres especiales (tildes, ñ, etc.)")
                
                # Eliminar archivo original después de conversión exitosa
                self.safe_delete_file(file_path)
            else:
                self.log_event(f"Error en conversión: {result.stderr}")
                
        except Exception as e:
            self.log_event(f"Excepción durante conversión: {str(e)}")
    
    def process_file_debounced(self, file_path):
        """Procesa archivo con debouncing para evitar procesamiento múltiple"""
        with self.timer_lock:
            # Cancelar timer anterior si existe
            if file_path in self.pending_timers:
                self.pending_timers[file_path].cancel()
                self.log_event(f"Cancelando procesamiento previo de: {os.path.basename(file_path)}")
            
            # Crear nuevo timer con delay de 3 segundos
            def delayed_conversion():
                try:
                    with self.timer_lock:
                        # Limpiar el timer del diccionario
                        if file_path in self.pending_timers:
                            del self.pending_timers[file_path]
                    
                    # Verificar que el archivo sigue existiendo y no se ha procesado
                    if os.path.exists(file_path):
                        # Usar timestamp para evitar re-procesar el mismo archivo
                        file_key = f"{file_path}_{int(os.path.getmtime(file_path))}"
                        
                        # Verificar si ya fue procesado (para archivos que no se eliminaron por error)
                        if file_key not in self.processed_files:
                            self.convert_file(file_path)
                            # Nota: No agregamos a processed_files porque el archivo será eliminado
                            # Solo rastreamos archivos que fallaron al eliminarse
                            if os.path.exists(file_path):
                                self.processed_files.add(file_key)
                                self.log_event(f"⚠️  Archivo procesado pero no eliminado - marcado como procesado")
                        else:
                            self.log_event(f"Archivo ya procesado: {os.path.basename(file_path)}")
                    else:
                        self.log_event(f"Archivo eliminado antes del procesamiento: {os.path.basename(file_path)}")
                        
                except Exception as e:
                    self.log_event(f"Error en procesamiento diferido: {str(e)}")
            
            # Crear y iniciar timer
            timer = threading.Timer(3.0, delayed_conversion)
            self.pending_timers[file_path] = timer
            timer.start()
            
            self.log_event(f"Programado para procesar en 3s: {os.path.basename(file_path)}")
    
    def on_created(self, event):
        """Se ejecuta cuando se crea un nuevo archivo"""
        if not event.is_directory and self.is_word_file(event.src_path):
            self.log_event(f"Nuevo archivo detectado: {os.path.basename(event.src_path)}")
            self.process_file_debounced(event.src_path)
    
    def on_modified(self, event):
        """Se ejecuta cuando se modifica un archivo"""
        if not event.is_directory and self.is_word_file(event.src_path):
            self.log_event(f"Archivo modificado: {os.path.basename(event.src_path)}")
            self.process_file_debounced(event.src_path)
    
    def on_moved(self, event):
        """Se ejecuta cuando se mueve/renombra un archivo"""
        if not event.is_directory and self.is_word_file(event.dest_path):
            self.log_event(f"Archivo movido: {os.path.basename(event.dest_path)}")
            self.process_file_debounced(event.dest_path)

def scan_existing_files(watch_dir, handler):
    """Escanea archivos existentes en la carpeta"""
    print("Escaneando archivos existentes...")
    
    for file_path in Path(watch_dir).glob("*.docx"):
        if handler.is_word_file(str(file_path)):
            print(f"Procesando archivo existente: {file_path.name}")
            handler.convert_file(str(file_path))
            # Nota: No agregamos a processed_files porque el archivo será eliminado
            # Solo rastrear si falló la eliminación
            if os.path.exists(str(file_path)):
                file_key = f"{str(file_path)}_{int(os.path.getmtime(str(file_path)))}"
                handler.processed_files.add(file_key)
                print(f"⚠️  Archivo {file_path.name} procesado pero no eliminado")

def main():
    # Directorio a monitorear (directorio actual del script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    watch_directory = script_dir
    
    print("=" * 60)
    print("    MONITOR AUTOMATICO WORD -> HTML OPTIMIZADO")
    print("=" * 60)
    print(f"Monitoreando: {watch_directory}")
    print("Funciones:")
    print("   - Detecta nuevos archivos .docx automáticamente")
    print("   - Convierte solo a <div> HTML en portapapeles")
    print("   - Elimina archivos originales después del procesamiento")
    print("   - Soporte completo UTF-8 (ñ, tildes, etc.)")
    print("   - Ignora archivos temporales de Word (~$)")
    print()
    print("Para detener: Ctrl+C")
    print("=" * 60)
    print()
    
    # Verificar dependencias
    try:
        import watchdog
        import mammoth
        import bs4
    except ImportError as e:
        print(f"Falta dependencia: {e}")
        print("Instala con: pip install watchdog mammoth beautifulsoup4")
        return
    
    # Crear manejador de eventos
    event_handler = WordFileHandler(script_dir)
    
    # Escanear archivos existentes
    scan_existing_files(watch_directory, event_handler)
    print()
    
    # Configurar observador
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=False)
    
    try:
        # Iniciar monitoreo
        observer.start()
        print("Monitor iniciado. Esperando archivos Word...")
        print()
        
        # Mantener el script ejecutándose
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDeteniendo monitor...")
        observer.stop()
        
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        observer.stop()
    
    observer.join()
    print("Monitor detenido.")

if __name__ == "__main__":
    main()