# Snake Retro — Instalación y configuración

## 1. Descripción del proyecto

Snake Retro es un juego web desarrollado con HTML, CSS y JavaScript.
Para el Reto 3 se incorporó un backend con Flask y una base de datos
MariaDB/MySQL para registrar partidas y consultar clasificaciones.

La aplicación contempla tres clasificaciones:
- Mejores puntuaciones históricas.
- Mayor tiempo de supervivencia.
- Mejores puntuaciones de los últimos siete días.

## 2. Tecnologías y versiones

Entorno verificado durante el desarrollo:

- Python: 3.13.1
- Flask: 3.1.3
- PyMySQL: 1.2.3
- Flask-Cors: 6.0.5
- MariaDB: 10.4.32
- Servidor web local: Python http.server
- Base de datos: snake_retro

Las versiones de Python y de las dependencias corresponden
al entorno de desarrollo utilizado para las pruebas.

## 3. Requisitos previos

- Windows.
- Python instalado.
- XAMPP con MariaDB/MySQL.
- Navegador web actualizado.
- Archivos del proyecto descargados desde la rama reto3-mejoras.

## 4. Configuración de la base de datos

1. Iniciar MySQL desde XAMPP.
2. Abrir http://localhost/phpmyadmin
3. Abrir la pestaña SQL.
4. Ejecutar el contenido de database/schema.sql.
5. Verificar la creación de la base de datos snake_retro.

El esquema crea las tablas:

- players: identificadores anónimos y apodos.
- games: puntuación, supervivencia, nivel y fecha de la partida.

En el entorno de desarrollo utilizado, MariaDB escucha en el
puerto 3307. Si la instalación utiliza otro puerto, debe ajustarse
la variable DB_PORT.

## 5. Instalación del backend

Abrir CMD en la carpeta raíz del proyecto.

Crear el entorno virtual:

    py -m venv .venv

Activarlo en Windows:

    .venv\Scripts\activate

Instalar las dependencias:

    python -m pip install -r backend\requirements.txt

Para verificar las versiones instaladas:

    python -m pip show Flask PyMySQL Flask-Cors

## 6. Configuración de conexión

El backend lee estas variables de entorno:

- DB_HOST: dirección del servidor de base de datos.
- DB_PORT: puerto de MariaDB/MySQL.
- DB_USER: usuario de la base de datos.
- DB_PASSWORD: contraseña configurada para ese usuario.
- DB_NAME: nombre de la base de datos.

Valores utilizados por defecto para las pruebas locales:

- DB_HOST: 127.0.0.1
- DB_PORT: 3307
- DB_NAME: snake_retro

El usuario y la contraseña deben corresponder a la configuración
local de MariaDB/MySQL. No se deben publicar credenciales reales.

## 7. Iniciar y verificar el backend

Con el entorno virtual activo, ejecutar:

    python backend\app.py

El servidor API utiliza por defecto:

    http://127.0.0.1:5000

Comprobar la conexión con la base de datos en:

    http://127.0.0.1:5000/api/health

La respuesta debe incluir el estado "ok" y el nombre de la
base de datos cuando la conexión se realiza correctamente.

## 8. Iniciar el frontend

Abrir una segunda ventana de CMD en la carpeta raíz del proyecto.

Ejecutar:

    py -m http.server 8000 --bind 127.0.0.1

Abrir el juego en:

    http://127.0.0.1:8000/index.html

Mantener abiertas las ventanas de CMD mientras se realizan
las pruebas locales.

## 9. Endpoints de la API

- GET /api/health: comprueba la conexión a la base de datos.
- POST /api/games: registra una partida.
- GET /api/leaderboard/points: consulta puntuaciones históricas.
- GET /api/leaderboard/survival: consulta tiempos de supervivencia.
- GET /api/leaderboard/weekly: consulta puntuaciones de los últimos
  siete días.

Las rutas de clasificación admiten el parámetro limit.

## 10. Consideraciones

El entorno descrito es local y sirve para desarrollo y evaluación.
Para permitir que usuarios externos compartan clasificaciones,
el backend y la base de datos deberán desplegarse en una infraestructura
accesible por Internet y configurarse de forma segura.

El identificador anónimo se almacena en el navegador. No equivale
a una cuenta verificada y puede perderse al borrar los datos del
navegador o cambiar de dispositivo.
