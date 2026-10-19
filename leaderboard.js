
(() => {
  "use strict";

  const API_BASE = "http://127.0.0.1:5000/api";
  const PLAYER_KEY_STORAGE = "snakeRetroPlayerKey_v1";

  const rankings = {
    points: {
      endpoint: "points",
      label: "Puntos",
      metric: (row) => `${row.score} pts`
    },
    survival: {
      endpoint: "survival",
      label: "Supervivencia",
      metric: (row) => `${Number(row.survival_seconds).toFixed(1)} s`
    },
    weekly: {
      endpoint: "weekly",
      label: "Semanal",
      metric: (row) => `${row.score} pts`
    }
  };

  let selectedRanking = "points";

  function getPlayerKey() {
    let key = localStorage.getItem(PLAYER_KEY_STORAGE);

    if (!key) {
      if (window.crypto && typeof crypto.randomUUID === "function") {
        key = crypto.randomUUID();
      } else {
        key = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
          /[xy]/g,
          (character) => {
            const random = Math.random() * 16 | 0;
            const value = character === "x" ? random : (random & 3 | 8);
            return value.toString(16);
          }
        );
      }

      localStorage.setItem(PLAYER_KEY_STORAGE, key);
    }

    return key;
  }

  function createLeaderboard() {
    const sidebar = document.querySelector(".sidebar");

    if (!sidebar) return;

    const card = document.createElement("section");
    card.className = "card";
    card.id = "globalLeaderboard";

    card.innerHTML = `
      <div class="card-header">
        <h2>Clasificación mundial</h2>
        <span id="globalRankingStatus" class="muted-small">Cargando...</span>
      </div>

      <div class="buttons">
        <button type="button" class="secondary"
          data-ranking="points">Puntos</button>
        <button type="button" class="secondary"
          data-ranking="survival">Supervivencia</button>
        <button type="button" class="secondary"
          data-ranking="weekly">Semanal</button>
      </div>

      <ol id="globalRankingList"
        style="margin:12px 0 0;padding-left:24px;line-height:1.8;
               font-size:12px;overflow-wrap:anywhere">
      </ol>
    `;

    const footer = sidebar.querySelector(".sidebar-footer");
    sidebar.insertBefore(card, footer || null);

    card.querySelectorAll("[data-ranking]").forEach((button) => {
      button.addEventListener("click", () => {
        selectedRanking = button.dataset.ranking;
        loadRanking(selectedRanking);
      });
    });

    loadRanking(selectedRanking);
  }

  async function loadRanking(type) {
    const list = document.getElementById("globalRankingList");
    const status = document.getElementById("globalRankingStatus");
    const config = rankings[type];

    if (!list || !status || !config) return;

    selectedRanking = type;
    status.textContent = "Consultando...";
    list.replaceChildren();

    try {
      const response = await fetch(
        `${API_BASE}/leaderboard/${config.endpoint}?limit=10`
      );

      if (!response.ok) {
        throw new Error("No se pudo consultar la clasificación");
      }

      const data = await response.json();

      if (!data.results || data.results.length === 0) {
        const item = document.createElement("li");
        item.textContent = "Aún no hay partidas.";
        list.appendChild(item);
      } else {
        data.results.forEach((row) => {
          const item = document.createElement("li");
          item.textContent =
            `${row.nickname} — ${config.metric(row)}`;
          list.appendChild(item);
        });
      }

      status.textContent = "Conectado";
    } catch (error) {
      console.error("Error de clasificación:", error);
      status.textContent = "Sin conexión";

      const item = document.createElement("li");
      item.textContent =
        "No se pudo consultar el servidor. Comprueba Flask.";
      list.appendChild(item);
    }
  }

  async function submitGame(detail) {
    const status = document.getElementById("globalRankingStatus");

    try {
      const response = await fetch(`${API_BASE}/games`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          player_key: getPlayerKey(),
          nickname: detail.nickname,
          score: Number(detail.score),
          survival_seconds: Number(detail.survival_seconds),
          level_reached: Number(detail.level_reached)
        })
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "No se pudo guardar la partida");
      }

      if (status) status.textContent = "Partida guardada";
      await loadRanking(selectedRanking);
    } catch (error) {
      console.error("Error al guardar la partida:", error);

      if (status) status.textContent = "Error al guardar";
    }
  }

  window.addEventListener("snake:gameover", (event) => {
    if (event.detail) submitGame(event.detail);
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", createLeaderboard);
  } else {
    createLeaderboard();
  }
})();
