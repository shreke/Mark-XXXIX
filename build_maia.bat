@echo off
echo Compilando MAIA...
if exist MAIA.spec del MAIA.spec
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
python -m PyInstaller --onedir --windowed --name MAIA --add-data "core;core" --add-data "config;config" --add-data "memory;memory" --add-data "actions;actions" --add-data "agent;agent" --add-data "auth;auth" --icon=maia.ico main.py
echo.
echo Listo! El ejecutable esta en dist\MAIA\MAIA.exe
pause
