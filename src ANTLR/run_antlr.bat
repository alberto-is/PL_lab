@echo off
REM Definir la ruta del JAR de ANTLR
set ANTLR_JAR="C:/antlr4/lib/antlr-4.7.2-complete.jar"

REM Verificar si el archivo JAR existe
if not exist %ANTLR_JAR% (
    echo El archivo %ANTLR_JAR% no se encontró.
    exit /b 1
)

REM Paso 1: Generar archivos Java
echo Generando archivos Java a partir de maze.g4...
java -jar %ANTLR_JAR% -listener -visitor -Dlanguage=Java -o "src ANTLR" "src ANTLR/maze.g4"
if %errorlevel% neq 0 (
    echo Error al generar archivos Java.
    exit /b 1
)

REM Paso 2: Compilar los archivos Java
echo Compilando archivos Java...
cd "src ANTLR"
javac -cp ".;%ANTLR_JAR%" *.java -d .antlr
if %errorlevel% neq 0 (
    echo Error al compilar los archivos Java.
    exit /b 1
)


REM Paso 3: Ejecutar el programa principal
echo Ejecutando el programa Main...

java -cp ".;%ANTLR_JAR%;.antlr" Main "ejemplos/ej_maze_incorrecto_semantica.txt"
if %errorlevel% neq 0 (
    echo Error al ejecutar el programa.
    exit /b 1
)


