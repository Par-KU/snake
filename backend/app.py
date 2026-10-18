
import os

import pymysql
from pymysql.cursors import DictCursor
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Permitimos solicitudes desde los dominios locales
# que usaremos durante las pruebas.
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost",
                "http://127.0.0.1",
                "http://snake.test",
            ]
        }
    },
)


def get_db_connection():
    """Abre una conexión con la base de datos Snake Retro."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "snake_retro"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        connect_timeout=5,
        autocommit=False,
    )


@app.get("/")
def home():
    return jsonify({
        "application": "Snake Retro API",
        "health_endpoint": "/api/health",
    })


@app.get("/api/health")
def health():
    """Comprueba que Flask puede conectarse a MySQL."""
    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DATABASE() AS database_name, "
                "VERSION() AS mysql_version"
            )
            result = cursor.fetchone()

        return jsonify({
            "status": "ok",
            "database": result["database_name"],
            "mysql_version": result["mysql_version"],
        }), 200

    except pymysql.MySQLError:
        app.logger.exception("Error al conectar con MySQL")

        return jsonify({
            "status": "error",
            "message": (
                "No se pudo conectar con MySQL. "
                "Revisa el servicio, el puerto y las variables DB_*."
            ),
        }), 503

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=False,
    )
