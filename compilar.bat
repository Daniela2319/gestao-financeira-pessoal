@echo off
REM Script para compilar o aplicativo em .exe com PyInstaller

echo ========================================
echo  Compilando Sistema de Controle de Despesas
echo ========================================
echo.

REM Ativar ambiente virtual
call .\venv\Scripts\activate.bat

REM Executar PyInstaller
echo Gerando executavel com PyInstaller...
pyinstaller --onefile --windowed --icon=app_icon.ico --name="Controle-Despesas" main.py

echo.
echo ========================================
echo  Compilacao concluida!
echo ========================================
echo.
echo O arquivo .exe esta em: dist\Controle-Despesas.exe
echo.
pause
