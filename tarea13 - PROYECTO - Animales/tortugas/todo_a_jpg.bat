@echo off
REM ==========================================
REM  Script para convertir imágenes a .jpg
REM  Requiere tener FFmpeg en el PATH
REM  Mantiene fechas de creación/modificación
REM ==========================================

setlocal enabledelayedexpansion

echo Convirtiendo archivos de imagen a .jpg...
echo (Excluyendo archivos JPG existentes)
echo ------------------------------------------

set /a converted=0
set /a skipped=0

REM Procesar archivos. Nota: Agregué comillas en el set para manejar espacios mejor
for %%i in (*.png *.bmp *.tiff *.tif *.webp *.avif *.heic *.jpeg *.gif) do (
    set "filename=%%~ni"
    set "extension=%%~xi"
    
    REM Verificar si ya existe un archivo JPG con el mismo nombre
    if not exist "!filename!.jpg" (
        echo Procesando: "%%i"
        
        REM 1. Convertir la imagen con ffmpeg
        REM -loglevel error reduce el texto en pantalla para que se vea limpio
        ffmpeg -loglevel error -y -i "%%i" "!filename!.jpg"
        
        REM 2. Usar PowerShell para copiar la fecha del archivo original al nuevo
        REM Esto copia CreationTime y LastWriteTime
        powershell -NoProfile -Command "$src = Get-Item '%%i'; $dst = Get-Item '!filename!.jpg'; $dst.CreationTime = $src.CreationTime; $dst.LastWriteTime = $src.LastWriteTime"
        
        set /a converted+=1
    ) else (
        echo Saltando: "%%i" (ya existe !filename!.jpg)
        set /a skipped+=1
    )
)

echo ------------------------------------------
echo Conversion completada.
echo Archivos convertidos: !converted!
echo Archivos omitidos: !skipped!
pause