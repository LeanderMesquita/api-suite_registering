@echo off
REM Abrir a pasta "automation_pattern" no Desktop
cd "%USERPROFILE%\Desktop\automation_pattern"

REM Ativar o ambiente virtual
call .venv\Scripts\activate

REM Entrar na subpasta "api"
cd api

REM Abrir um terminal e executar 'flask run'
start cmd /k "flask run"
