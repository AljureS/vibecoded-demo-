param([string]$ExtensionArchivos = "*.docx")

$CarpetaScript    = Split-Path -Parent $MyInvocation.MyCommand.Path
$CarpetaMonitoreo = $CarpetaScript
$ScriptEjecutar   = Join-Path $CarpetaScript "auto_word_watcher.py"

Write-Host ''
Write-Host 'SSSSS   AAA   III  DDD   ' -ForegroundColor Green
Write-Host 'S      A   A   I   D   D  ' -ForegroundColor Green  
Write-Host 'SSSSS  AAAAA   I   D   D  ' -ForegroundColor Green
Write-Host '    S  A   A   I   D   D  ' -ForegroundColor Green
Write-Host 'SSSSS  A   A  III  DDD   ' -ForegroundColor Green
Write-Host ''
Write-Host 'EEEEE  SSSSS  TTTTT  U   U  V   V  OOO  ' -ForegroundColor Yellow
Write-Host 'E      S        T    U   U  V   V  O   O' -ForegroundColor Yellow
Write-Host 'EEEEE  SSSSS    T    U   U  V   V  O   O' -ForegroundColor Yellow  
Write-Host 'E          S    T    U   U   V V   O   O' -ForegroundColor Yellow
Write-Host 'EEEEE  SSSSS    T     UUU     V    OOO  ' -ForegroundColor Yellow
Write-Host ''
Write-Host ' AAA    CCC    AAA   ' -ForegroundColor Cyan
Write-Host 'A   A  C      A   A  ' -ForegroundColor Cyan
Write-Host 'AAAAA  C      AAAAA  ' -ForegroundColor Cyan
Write-Host 'A   A  C      A   A  ' -ForegroundColor Cyan
Write-Host 'A   A   CCC   A   A  ' -ForegroundColor Cyan
Write-Host ''
Write-Host '       MONITOR WORD -> HTML       ' -ForegroundColor Red
Write-Host '===================================' -ForegroundColor White
Write-Host ''

if (-not (Test-Path $ScriptEjecutar)) {
    Write-Host 'Error: No se encontro auto_word_watcher.py' -ForegroundColor Red
    Read-Host 'Presiona Enter'
    exit 1
}

Write-Host "Ejecutando monitor Python..." -ForegroundColor Green
Write-Host 'Presiona Ctrl+C para detener' -ForegroundColor Yellow
Write-Host ''

try {
    & python $ScriptEjecutar
}
catch {
    Write-Host "Error ejecutando el monitor: $_" -ForegroundColor Red
}
finally {
    Write-Host 'Monitor detenido' -ForegroundColor Red
}