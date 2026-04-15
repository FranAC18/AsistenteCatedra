@echo off
echo Creando estructura del proyecto...

:: Proteccion si la carpeta ya existe

mkdir backend
mkdir backend\utils

mkdir frontend
mkdir frontend\assets

mkdir data

:: Backend files
type nul > backend\__init__.py
type nul > backend\main.py
type nul > backend\bridge.py
type nul > backend\config.py
type nul > backend\prompt.py
type nul > backend\history.py
type nul > backend\audio_input.py
type nul > backend\speech_to_text.py
type nul > backend\text_cleaning.py
type nul > backend\tokenizer.py
type nul > backend\llm_client.py
type nul > backend\text_to_speech.py

:: Utils package
type nul > backend\utils\__init__.py

:: Frontend files
type nul > frontend\index.html
type nul > frontend\styles.css
type nul > frontend\app.js

:: Data files — JSON valido para no romper el parser
echo [] > data\history.json
echo {} > data\settings.json

:: Root files
type nul > requirements.txt
type nul > run_project.py

echo.
echo Estructura creada correctamente.
echo.
tree /f
pause