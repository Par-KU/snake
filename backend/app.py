import os
import uuid

import pymysql
from pymysql.cursors import DictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

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
        })

    except pymysql.MySQLError:
        app.logger.exception("Error al conectar con MySQL")
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar con MySQL.",
        }), 503

    finally:
        if connection is not None:
            connection.close()


@app.post("/api/games")
def save_game():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Se requiere un objeto JSON."}), 400

    player_key = data.get("player_key")
    nickname = data.get("nickname")
    score = data.get("score")
    survival = data.get("survival_seconds")
    level = data.get("level_reached")

    if not isinstance(player_key, str):
        return jsonify({"error": "Identificador inválido."}), 400

    try:
        player_key = str(uuid.UUID(player_key))
    except (ValueError, AttributeError):
        return jsonify({"error": "El identificador debe ser un UUID."}), 400

    if not isinstance(nickname, str):
        return jsonify({"error": "El apodo es obligatorio."}), 400

    nickname = nickname.strip()

    if not nickname or len(nickname) > 18:
        return jsonify({
            "error": "El apodo debe tener entre 1 y 18 caracteres."
        }), 400

    if type(score) is not int or not 0 <= score <= 10_000_000:
        return jsonify({"error": "Puntuación inválida."}), 400

    if type(level) is not int or not 1 <= level <= 10:
        return jsonify({"error": "Nivel inválido."}), 400

    if isinstance(survival, bool) or not isinstance(
        survival, (int, float)
    ):
        return jsonify({"error": "Tiempo de supervivencia inválido."}), 400

    if not 0 <= survival <= 86400:
        return jsonify({"error": "Tiempo fuera del rango permitido."}), 400

    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO players (player_key, nickname)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE nickname = VALUES(nickname)
                """,
                (player_key, nickname),
            )

            cursor.execute(
                "SELECT id FROM players WHERE player_key = %s",
                (player_key,),
            )
            player = cursor.fetchone()

            cursor.execute(
                """
                INSERT INTO games
                    (player_id, score, survival_seconds, level_reached)
                VALUES (%s, %s, %s, %s)
                """,
                (player["id"], score, survival, level),
            )

            game_id = cursor.lastrowid

        connection.commit()

        return jsonify({
            "status": "saved",
            "game_id": game_id,
            "nickname": nickname,
        }), 201

    except pymysql.MySQLError:
        if connection is not None:
            connection.rollback()

        app.logger.exception("Error al guardar una partida")
        return jsonify({
            "error": "No se pudo guardar la partida."
        }), 503

    finally:
        if connection is not None:
            connection.close()


def get_limit():
    limit = request.args.get("limit", default=10, type=int)

    if limit is None:
        limit = 10

    return max(1, min(limit, 50))


def leaderboard_response(query, params, ranking, period):
    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        for row in results:
            if "survival_seconds" in row:
                row["survival_seconds"] = float(
                    row["survival_seconds"]
                )

        return jsonify({
            "ranking": ranking,
            "period": period,
            "results": results,
        })

    except pymysql.MySQLError:
        app.logger.exception("Error al consultar la clasificación")
        return jsonify({
            "error": "No se pudo consultar la clasificación."
        }), 503

    finally:
        if connection is not None:
            connection.close()


@app.get("/api/leaderboard/points")
def leaderboard_points():
    query = """
        SELECT p.nickname, MAX(g.score) AS score
        FROM games AS g
        JOIN players AS p ON p.id = g.player_id
        GROUP BY p.id, p.nickname
        ORDER BY score DESC, p.nickname ASC
        LIMIT %s
    """

    return leaderboard_response(
        query,
        (get_limit(),),
        "points",
        "all_time",
    )


@app.get("/api/leaderboard/survival")
def leaderboard_survival():
    query = """
        SELECT
            p.nickname,
            MAX(g.survival_seconds) AS survival_seconds
        FROM games AS g
        JOIN players AS p ON p.id = g.player_id
        GROUP BY p.id, p.nickname
        ORDER BY survival_seconds DESC, p.nickname ASC
        LIMIT %s
    """

    return leaderboard_response(
        query,
        (get_limit(),),
        "survival",
        "all_time",
    )


@app.get("/api/leaderboard/weekly")
def leaderboard_weekly():
    query = """
        SELECT p.nickname, MAX(g.score) AS score
        FROM games AS g
        JOIN players AS p ON p.id = g.player_id
        WHERE g.played_at >=
            DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY p.id, p.nickname
        ORDER BY score DESC, p.nickname ASC
        LIMIT %s
    """

    return leaderboard_response(
        query,
        (get_limit(),),
        "weekly",
        "last_7_days",
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=False,
    )
