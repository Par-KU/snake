# Snake Retro — Instalación y configuración

## 1. Descripción del proyecto

Snake Retro es una aplicación web desarrollada con HTML, CSS y JavaScript. Para el Reto 3 se incorporó una API desarrollada con Flask y una base de datos MariaDB compatible con MySQL.

La aplicación registra las partidas y muestra tres clasificaciones: puntuación histórica, tiempo de supervivencia y puntuaciones de los últimos siete días.

El proyecto se desarrolló en Windows, utilizando XAMPP, Apache, OpenSSL y un entorno virtual de Python. Los cambios del reto se encuentran en la rama `reto3-mejoras`, mientras que la rama `main` conserva la versión original.

## 2. Tecnologías y versiones

Versiones verificadas durante las pruebas locales:

- Python: 3.13.1
- Flask: 3.1.3
- PyMySQL: 1.2.3
- Flask-Cors: 6.0.5
- MariaDB: 10.4.32
- Apache HTTP Server: 2.4.58
- OpenSSL: 3.1.3

Tecnologías adicionales:

- HTML5, CSS y JavaScript.
- XAMPP y phpMyAdmin.
- Apache VirtualHosts y proxy inverso.
- Certificado SSL/TLS autofirmado.
- Lighthouse para evaluación de rendimiento.

Las versiones anteriores corresponden al entorno utilizado para las pruebas. El archivo `backend/requirements.txt` declara rangos de versiones compatibles para las dependencias de Python.

## 3. Requisitos previos

Para reproducir la configuración local se requiere:

- Windows.
- Python instalado.
- XAMPP con Apache y MariaDB/MySQL.
- Un navegador actualizado.
- Los archivos del proyecto descargados desde la rama `reto3-mejoras` del repositorio.

Repositorio: https://github.com/Par-KU/snake/tree/reto3-mejoras

Antes de iniciar las pruebas, debe comprobarse que los puertos 80 y 443 estén disponibles para Apache, el puerto 3307 para MariaDB en la configuración utilizada y el puerto 5000 para Flask.

Los puertos pueden cambiar según la instalación local. Si se modifican, también deberán actualizarse las configuraciones correspondientes.

## 4. Configuración de la base de datos

### 4.1. Iniciar MariaDB

1. Abrir XAMPP Control Panel.
2. Iniciar el servicio de MySQL.
3. Abrir phpMyAdmin desde XAMPP o mediante `http://localhost/phpmyadmin`.

En el entorno original, MariaDB se encuentra disponible en el puerto 3307.

### 4.2. Crear las tablas

En phpMyAdmin:

1. Abrir la pestaña SQL.
2. Ejecutar el contenido de `database/schema.sql`.
3. Confirmar la creación de la base de datos `snake_retro`.
4. Verificar que existan las tablas `players` y `games`.

La tabla `players` almacena el identificador anónimo, el apodo y la fecha de creación. La tabla `games` almacena los puntos, el tiempo de supervivencia, el nivel alcanzado y la fecha de la partida.

La relación entre ambas tablas permite asociar cada partida con su jugador. El esquema incluye índices para facilitar las consultas por puntuación, supervivencia y fecha.

El script utiliza `CREATE DATABASE IF NOT EXISTS` y `CREATE TABLE IF NOT EXISTS`, por lo que puede ejecutarse nuevamente sin recrear las tablas existentes. No elimina los registros anteriores.

## 5. Instalación del backend

Abrir CMD en la carpeta raíz del proyecto, donde se encuentran `index.html`, `backend` y `database`.

Crear el entorno virtual:

    py -m venv .venv

Activar el entorno virtual:

    .venv\Scripts\activate

Instalar las dependencias:

    python -m pip install -r backend\requirements.txt

Comprobar las versiones instaladas:

    python --version
    python -m pip show Flask PyMySQL Flask-Cors

El entorno virtual mantiene las dependencias separadas de las instalaciones globales de Python.

## 6. Configuración de la conexión a MariaDB

El backend utiliza las siguientes variables de entorno:

- `DB_HOST`: dirección del servidor de base de datos.
- `DB_PORT`: puerto de MariaDB/MySQL.
- `DB_USER`: usuario de la base de datos.
- `DB_PASSWORD`: contraseña del usuario.
- `DB_NAME`: nombre de la base de datos.
- `FLASK_PORT`: puerto de ejecución del backend.

Los valores predeterminados definidos por la aplicación son:

- `DB_HOST=127.0.0.1`
- `DB_PORT=3307`
- `DB_NAME=snake_retro`
- `FLASK_PORT=5000`

El usuario y la contraseña deben corresponder a la configuración real de MariaDB/MySQL. En una instalación local donde el usuario `root` no tenga contraseña, el parámetro `DB_PASSWORD` puede permanecer vacío. Si se configuró una contraseña, debe establecerse mediante la variable de entorno correspondiente.

No se deben publicar contraseñas reales en GitHub.

## 7. Iniciar y comprobar Flask

Con MariaDB activo y el entorno virtual habilitado, ejecutar desde la raíz del proyecto:

    python backend\app.py

Por defecto, Flask escucha en:

    http://127.0.0.1:5000

Para comprobar la conexión con MariaDB, abrir:

    http://127.0.0.1:5000/api/health

La respuesta esperada contiene el estado `ok`, el nombre de la base de datos y la versión del servidor.

Si la respuesta indica un error de conexión, comprobar que MariaDB esté activo y que el puerto, el usuario y la contraseña sean correctos.

Mantener abierta la consola de Flask durante las pruebas.

## 8. Configuración del dominio local

La aplicación utiliza el dominio de pruebas `snake.test`, asociado a `127.0.0.1` en el archivo `hosts` de Windows.

El archivo se encuentra en:

    C:\Windows\System32\drivers\etc\hosts

Para configurar el dominio en un equipo nuevo:

1. Abrir el Bloc de notas como administrador.
2. Abrir el archivo `hosts`, seleccionando la opción para mostrar todos los archivos.
3. Añadir la siguiente línea, si todavía no existe:

       127.0.0.1 snake.test

4. Guardar los cambios.

Este dominio es local: no publica la aplicación en Internet ni hace que sea accesible desde otros equipos automáticamente.

## 9. Configuración de Apache y HTTPS

### 9.1. Activación de módulos

En la configuración de Apache, comprobar que estén habilitados los módulos necesarios para SSL, encabezados de seguridad, reescritura y proxy HTTP. En la instalación utilizada se verificaron, entre otros:

- `headers_module`
- `proxy_module`
- `proxy_http_module`
- `rewrite_module`

También debe estar habilitada la inclusión de la configuración de VirtualHosts.

### 9.2. Certificado local

Para las pruebas se generó un certificado autofirmado con OpenSSL. Los archivos se guardaron fuera del repositorio, en:

    C:\xampp\apache\conf\snake-ssl\

Los nombres utilizados fueron:

- `snake.test.crt`: certificado.
- `snake.test.key`: clave privada.

La clave privada no debe incluirse en el ZIP del proyecto ni subirse a GitHub. Para reproducir esta configuración en otro equipo, se debe generar un certificado propio y actualizar las rutas correspondientes.

Un certificado autofirmado permite probar HTTPS de forma local, pero el navegador puede advertir que no confía en su emisor. Esta configuración no sustituye un certificado emitido por una autoridad de confianza pública.

### 9.3. VirtualHosts

El archivo utilizado para configurar los sitios fue:

    C:\xampp\apache\conf\extra\httpd-vhosts.conf

Se configuraron VirtualHosts independientes para `transcriptor.test` y `snake.test`. No se debe reemplazar todo el archivo en un equipo que ya tenga otros sitios; únicamente deben añadirse o adaptarse los bloques correspondientes.

En los bloques de Snake Retro, las directivas `DocumentRoot` y `<Directory>` deben apuntar a la carpeta real donde se extrajeron los archivos del proyecto. La ruta del equipo original no necesariamente coincide con la del equipo donde se reproduzca la configuración.

El VirtualHost HTTP redirige las solicitudes hacia HTTPS. El VirtualHost HTTPS utiliza el certificado local y las reglas de proxy inverso para reenviar las solicitudes `/api/` a Flask en `127.0.0.1:5000`.

La configuración debe conservar estas funciones:

- Redirección de HTTP a HTTPS.
- Entrega de archivos estáticos desde la carpeta del proyecto.
- Reenvío de `/api/` hacia Flask.
- Registro de accesos y errores de Apache.

### 9.4. Cabeceras de seguridad

El VirtualHost HTTPS de `snake.test` incluye las cabeceras:

- `Content-Security-Policy`
- `Strict-Transport-Security`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`

La política CSP restringe los recursos y las conexiones permitidos. HSTS solicita al navegador utilizar HTTPS durante el tiempo especificado en su directiva `max-age`.

### 9.5. Validar y reiniciar Apache

Después de modificar la configuración, ejecutar en CMD:

    C:\xampp\apache\bin\httpd.exe -t

El resultado esperado es:

    Syntax OK

Si la validación es correcta, reiniciar Apache desde XAMPP Control Panel.

Si Apache no inicia, revisar los mensajes del panel y los registros de errores antes de modificar más directivas.

## 10. Ejecutar y verificar la aplicación

Para utilizar la aplicación completa en el entorno configurado:

1. Iniciar MariaDB desde XAMPP.
2. Activar el entorno virtual de Python.
3. Ejecutar `python backend\app.py`.
4. Iniciar o reiniciar Apache desde XAMPP.
5. Abrir en el navegador:

       https://snake.test/

La aplicación utiliza `leaderboard.js` para consultar las clasificaciones mediante la ruta relativa `/api`. Apache reenvía esas solicitudes al backend Flask.

Para verificar la conexión mediante HTTPS, ejecutar:

    curl.exe -k -i https://snake.test/api/health

La opción `-k` permite efectuar esta comprobación con el certificado autofirmado. No instala el certificado como confiable ni modifica la configuración de seguridad del navegador.

La respuesta esperada es `200 OK` y un JSON que incluya el estado `ok` y la base de datos `snake_retro`.

Para comprobar la redirección de HTTP a HTTPS:

    curl.exe --noproxy "*" -I --resolve snake.test:80:127.0.0.1 http://snake.test/

La respuesta esperada es `301 Moved Permanently` con una cabecera `Location` que apunte a `https://snake.test/`.

Para comprobar las cabeceras de seguridad:

    curl.exe -k -I https://snake.test/

La respuesta debe incluir las cabeceras de seguridad configuradas en Apache.

## 11. Endpoints de la API

| Método | Ruta | Función |
|---|---|---|
| GET | `/api/health` | Verifica la conexión con la base de datos. |
| POST | `/api/games` | Registra una partida. |
| GET | `/api/leaderboard/points` | Consulta las puntuaciones históricas. |
| GET | `/api/leaderboard/survival` | Consulta los mayores tiempos de supervivencia. |
| GET | `/api/leaderboard/weekly` | Consulta puntuaciones de los últimos siete días. |

Las rutas de clasificación admiten el parámetro `limit` para limitar la cantidad de resultados.

## 12. Pruebas funcionales y de rendimiento

Las pruebas se realizaron en Google Chrome y Microsoft Edge. Se comprobó la carga del juego mediante HTTPS, la visualización de las clasificaciones y el funcionamiento de los controles principales.

Se utilizó Lighthouse en modo Navegación, dispositivo Escritorio y categoría Rendimiento. En la prueba registrada se obtuvo una puntuación de 100/100. Los resultados corresponden a la ejecución local y pueden variar según el dispositivo y las condiciones de prueba.

## 13. Consideraciones de seguridad y alcance

Esta instalación corresponde a un entorno local de desarrollo y evaluación. Para permitir que usuarios externos compartan las clasificaciones, sería necesario desplegar el backend y la base de datos en una infraestructura accesible por Internet y proteger adecuadamente el servicio.

El identificador almacenado en el navegador es anónimo y no verifica la identidad real del jugador. Puede perderse al borrar los datos locales o cambiar de dispositivo. Además, las puntuaciones no cuentan con una verificación completa contra trampas.

No deben compartirse certificados privados, contraseñas ni otros secretos. La configuración de Apache y del certificado debe adaptarse a cada equipo donde se reproduzca el proyecto.
