@echo off
chcp 65001 >nul
echo ==============================================================================
echo 🐾 PET GUARDIAN - INICIANDO SUÍTE OFICIAL DE DEMONSTRAÇÃO SPRINT 4
echo ==============================================================================

set PYTHON_CMD=

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 set PYTHON_CMD=python

if "%PYTHON_CMD%"=="" (
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PYTHON_CMD=py -3
)

if "%PYTHON_CMD%"=="" (
    if exist "C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe" (
        set "PYTHON_CMD=\"C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe\""
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERRO] Python não foi encontrado no PATH.
    echo Por favor execute: python deploy_guardianai_render\test_sprint4_scenarios.py --mode local
    pause
    exit /b 1
)

%PYTHON_CMD% deploy_guardianai_render\test_sprint4_scenarios.py --mode local --delay 0.8
pause
