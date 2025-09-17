# Contexto de Archivos del Proyecto - Sistema de Conversión Word a HTML

```xml
<proyecto>
    <nombre>Sistema de Conversión Automática Word a HTML</nombre>
    <descripcion>
        Sistema completo para monitorear carpetas y convertir automáticamente archivos de Microsoft Word (.docx) a HTML 
        con estilos CSS personalizados. Incluye funcionalidades de monitoreo en tiempo real, conversión manual y 
        aplicación de estilos personalizados.
    </descripcion>
    
    <arquitectura>
        <componente_principal>
            <archivo>auto_word_watcher.py</archivo>
            <tipo>Monitor Automático</tipo>
            <funcionalidad>
                - Monitorea carpeta en tiempo real usando watchdog
                - Detecta archivos .docx nuevos o modificados
                - Convierte automáticamente a HTML usando word_to_html.py
                - ELIMINA archivos .docx originales después del procesamiento exitoso
                - Sistema de eliminación segura con reintentos (3 intentos)
                - Manejo robusto de errores de permisos y archivos en uso
                - Ignora archivos temporales de Word (~$)
                - Debouncing avanzado para evitar procesamiento múltiple
                - Threading para conversiones simultáneas no bloqueantes
                - Sistema de logging detallado con timestamps y códigos de estado
                - Copia el HTML resultante al portapapeles
                - Tracking inteligente de archivos procesados (solo fallas de eliminación)
            </funcionalidad>
            <dependencias>watchdog, mammoth, beautifulsoup4</dependencias>
        </componente_principal>
        
        <convertidor_core>
            <archivo>word_to_html.py</archivo>
            <tipo>Convertidor Principal</tipo>
            <funcionalidad>
                - Convierte archivos .docx a HTML usando mammoth
                - SISTEMA DE VALIDACIÓN UTF-8 DE 4 CHECKPOINTS críticos
                - Corrección automática de corrupción de caracteres españoles
                - Detección y reparación de patrones: más→m├ís, ñ→├▒, etc.
                - Aplica CSS responsivo optimizado para integración web
                - Procesa HTML con BeautifulSoup sin warnings de encoding
                - Copia contenido HTML directamente al portapapeles (Windows)
                - Función safe_delete_file() con manejo robusto de errores
                - Soporte para conversión individual o por lotes de directorios
                - Generación de contenido limpio solo con div container
                - Salida de consola segura con safe_print() (anti-Unicode crash)
                - Validación estricta UTF-8 en todo el pipeline de procesamiento
            </funcionalidad>
            <dependencias>mammoth, beautifulsoup4</dependencias>
        </componiente_core>
        
        <estilos>
            <archivo>estilos_personalizados.css</archivo>
            <tipo>Hoja de Estilos CSS</tipo>
            <funcionalidad>
                - CSS responsivo MÍNIMO optimizado para integración Ticketmaster
                - Diseño que hereda propiedades del contenedor padre
                - Estilos no intrusivos que evitan conflictos de layout
                - Tipografía adaptable con font-family: inherit
                - Colores heredados del contexto de la página
                - Padding y margin controlados para integración web
                - Elementos responsive con max-width y line-height optimizados
            </funcionalidad>
        </estilos>
    </arquitectura>
    
    <scripts_lanzadores>
        <lanzador_bat>
            <archivo>iniciar_monitor.bat</archivo>
            <tipo>Script de Inicio Windows</tipo>
            <funcionalidad>
                - Verifica instalación de Python
                - Instala dependencias automáticamente si no existen
                - Lanza el monitor automático auto_word_watcher.py
                - Manejo de errores y mensajes informativos
                - Interface de usuario simple para Windows
            </funcionalidad>
        </lanzador_bat>
        
        <lanzador_ps1>
            <archivo>monitor.ps1</archivo>
            <tipo>Script PowerShell</tipo>
            <funcionalidad>
                - Script PowerShell con arte ASCII personalizado
                - Interfaz visual mejorada con colores
                - Verificación de archivos del sistema
                - Lanzamiento del monitor Python
                - Manejo de excepciones PowerShell
                - Banner personalizado "SAID ESTUVO ACA"
            </funcionalidad>
        </lanzador_ps1>
        
        <convertidor_manual>
            <archivo>word2html.bat</archivo>
            <tipo>Convertidor Manual</tipo>
            <funcionalidad>
                - Conversión manual de archivos individuales
                - Soporte para conversión por lotes de directorios
                - Verificación automática de dependencias
                - Instalación automática de paquetes Python
                - Interface de línea de comandos con múltiples opciones
                - Soporte para CSS personalizado
            </funcionalidad>
        </convertidor_manual>
    </scripts_lanzadores>
    
    <utilidades>
        <claude_shortcut>
            <archivo>claude-haiku.bat</archivo>
            <tipo>Atajo Claude</tipo>
            <funcionalidad>
                - Atajo para ejecutar Claude con modelo Haiku específico
                - Pasa todos los argumentos de línea de comandos
                - Simplifica el acceso a Claude Code
            </funcionalidad>
        </claude_shortcut>
        
        <documento_ejemplo>
            <archivo>V2 COMUNICADO OFICIAL-ANCESTRAL MX.docx</archivo>
            <tipo>Documento de Prueba</tipo>
            <funcionalidad>
                - Documento Word de ejemplo/prueba
                - Utilizado para validar el sistema de conversión
                - Contiene formato típico de documento oficial
            </funcionalidad>
        </documento_ejemplo>
        
        <configuracion_claude>
            <directorio>.claude</directorio>
            <tipo>Configuración Claude Code</tipo>
            <funcionalidad>
                - Contiene configuraciones para Claude Code
                - Settings y preferencias del usuario
                - Archivos de configuración del entorno
            </funcionalidad>
        </configuracion_claude>
    </utilidades>
    
    <flujo_trabajo>
        <automatico>
            1. Ejecutar iniciar_monitor.bat o monitor.ps1
            2. El sistema monitoreará la carpeta automáticamente
            3. Al detectar un archivo .docx, lo convertirá a HTML
            4. El HTML se copia automáticamente al portapapeles
            5. Se aplican estilos CSS responsivos integrados
            6. EL ARCHIVO .DOCX ORIGINAL SE ELIMINA AUTOMÁTICAMENTE
            7. Solo se conservan archivos que fallan al eliminarse (con aviso)
        </automatico>
        
        <manual>
            1. Ejecutar word2html.bat con el archivo deseado
            2. Por defecto: convierte + copia + ELIMINA el archivo original
            3. Usar --keep-original para conservar el archivo fuente
            4. Opcionalmente especificar archivo CSS personalizado
            5. El HTML se genera y se copia al portapapeles
            6. Sistema de validación UTF-8 en 4 checkpoints críticos
        </manual>
    </flujo_trabajo>
    
    <caracteristicas_tecnicas>
        <lenguajes>Python 3.x, CSS3, Batch, PowerShell</lenguajes>
        <plataforma>Windows (con soporte específico para clip.exe)</plataforma>
        <dependencias_python>watchdog, mammoth, beautifulsoup4</dependencias_python>
        <funcionalidades_clave>
            - Monitoreo en tiempo real de archivos con debouncing
            - Conversión automática Word a HTML con eliminación de originales
            - Sistema de validación UTF-8 en 4 checkpoints críticos
            - Corrección automática de corrupción de caracteres españoles
            - Estilos CSS responsivos optimizados para integración web
            - Copia automática al portapapeles con encoding estricto
            - Eliminación segura de archivos con sistema de reintentos
            - Procesamiento por lotes con tracking inteligente
            - Interface multiplataforma (BAT + PowerShell)
            - Manejo robusto de errores con códigos de estado
            - Sistema de logging detallado con timestamps y emojis
            - Compatibilidad con caracteres Unicode en consola Windows
        </funcionalidades_clave>
    </caracteristicas_tecnicas>
    
    <casos_uso>
        <primary>
            - Conversión automática de documentos Word para publicación web
            - Automatización de flujos de trabajo documentales
            - Procesamiento por lotes de documentos corporativos
            - Generación de contenido HTML estilizado desde Word
        </primary>
        <secondary>
            - Backup automático en formato web
            - Preparación de documentos para CMS
            - Conversión de comunicados oficiales a HTML
            - Procesamiento de documentación técnica
        </secondary>
    </casos_uso>
    
    <mejoras_recientes>
        <version>v2.0 - Eliminación Automática y UTF-8 Robusto</version>
        <fecha>2025-09-08</fecha>
        <cambios_criticos>
            <eliminacion_automatica>
                - Implementada eliminación automática de archivos .docx después del procesamiento exitoso
                - Función safe_delete_file() con sistema de reintentos (máximo 3 intentos)
                - Manejo robusto de errores PermissionError y archivos en uso
                - Logging detallado con indicadores de estado: ✅ éxito, ⚠️ advertencia, ❌ error
                - Tracking inteligente: solo se marcan como "procesados" los archivos que fallan al eliminarse
            </eliminacion_automatica>
            
            <validacion_utf8>
                - Sistema de 4 CHECKPOINTS críticos de validación UTF-8:
                  1. POST-MAMMOTH: Validación después de conversión mammoth
                  2. POST-BEAUTIFULSOUP: Validación después de procesamiento HTML
                  3. PRE-CLIPBOARD: Validación antes de copia al portapapeles  
                  4. PRE-SUBPROCESS: Validación final antes de subprocess clip.exe
                - Corrección automática de patrones de corrupción españoles:
                  más → m├ís, ñ → ├▒, é → ├⌐, á → ├í, etc.
                - Función safe_print() para evitar crashes Unicode en consola Windows
                - Validación estricta UTF-8 en todo el pipeline de procesamiento
            </validacion_utf8>
            
            <integracion_web>
                - CSS responsivo mínimo optimizado para integración Ticketmaster
                - Estilos que heredan propiedades del contenedor padre (font-family: inherit)
                - Eliminación de estilos intrusivos que causaban conflictos de layout
                - Padding y margin controlados para integración seamless
                - Max-width responsive y line-height optimizados
            </integracion_web>
            
            <mejoras_tecnicas>
                - Debouncing mejorado con threading.Timer para evitar procesamiento múltiple
                - Eliminación de warnings de BeautifulSoup relacionados con encoding
                - Corrección de caracteres Unicode en mensajes de consola (→ reemplazado por ->)
                - Manejo de excepciones mejorado en todas las operaciones de archivo
                - Tracking de archivos basado en timestamp para evitar reprocesamiento
                - Logging con timestamps y códigos de estado visuales
            </mejoras_tecnicas>
        </cambios_criticos>
        
        <comportamiento_actualizado>
            <modo_automatico>
                1. Monitor detecta archivo .docx → 2. Debouncing de 3 segundos → 
                3. Conversión a HTML → 4. Copia a portapapeles → 5. ELIMINACIÓN del .docx original
                - Solo se conservan archivos que fallan al eliminarse (con advertencia)
                - Sin acumulación de archivos procesados en el directorio
            </modo_automatico>
            
            <modo_manual>
                1. Por defecto: convierte + copia + ELIMINA archivo original
                2. Usar --keep-original para conservar el archivo fuente
                3. Validación UTF-8 en 4 checkpoints durante todo el proceso
                4. Corrección automática de caracteres corruptos detectados
            </modo_manual>
        </comportamiento_actualizado>
        
        <testing_realizado>
            - ✅ Conversión manual con eliminación automática
            - ✅ Monitor automático con detección y eliminación
            - ✅ Manejo de errores de permisos y archivos en uso
            - ✅ Validación UTF-8 en todos los checkpoints críticos
            - ✅ Corrección automática de caracteres españoles corruptos
            - ✅ Integración CSS responsiva sin conflictos de layout
            - ✅ Tracking inteligente de archivos procesados vs. eliminados
        </testing_realizado>
    </mejoras_recientes>
</proyecto>
```