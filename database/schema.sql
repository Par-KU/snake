-- Snake Retro - Esquema inicial de MySQL
-- Base de datos para registrar jugadores y partidas.

CREATE DATABASE IF NOT EXISTS snake_retro
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE snake_retro;

-- Jugadores identificados mediante un identificador anónimo
-- y un apodo. No se almacenan contraseñas.
CREATE TABLE IF NOT EXISTS players (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    player_key CHAR(36) NOT NULL UNIQUE,
    nickname VARCHAR(18) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_players_nickname (nickname)
) ENGINE=InnoDB;

-- Registro de las partidas.
CREATE TABLE IF NOT EXISTS games (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT UNSIGNED NOT NULL,
    score INT UNSIGNED NOT NULL DEFAULT 0,
    survival_seconds DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    level_reached TINYINT UNSIGNED NOT NULL DEFAULT 1,
    played_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_games_player
        FOREIGN KEY (player_id)
        REFERENCES players(id)
        ON DELETE CASCADE,

    INDEX idx_games_score (score),
    INDEX idx_games_survival (survival_seconds),
    INDEX idx_games_played_at (played_at),
    INDEX idx_games_player_played (player_id, played_at)
) ENGINE=InnoDB;
