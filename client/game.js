const game = document.getElementById("game");

const paddlePlayer1 = document.getElementById("paddle-player1");
const paddlePlayer2 = document.getElementById("paddle-player2");
const ball = document.getElementById("ball");

const socket = new WebSocket(`ws://${window.location.hostname}:8080`);

let meuJogador = null;

const scorePlayer1 = document.getElementById("score-player1");
const scorePlayer2 = document.getElementById("score-player2");

const status = document.getElementById("status");

// Tela de vitória
const gameOverScreen = document.getElementById("game-over");
const winnerMessage = document.getElementById("winner-message");
const finalScore = document.getElementById("final-score");
const restartButton = document.getElementById("restart-button");

// Posição das raquetes
let player1Y = 200;
let player2Y = 200;

// Posição da bola
let ballX = 390;
let ballY = 240;

// Placar
let player1Score = 0;
let player2Score = 0;

let gameOver = false;

// Controle das teclas
const keys = {};

document.addEventListener("keydown", (event) => {
  keys[event.key] = true;
});

document.addEventListener("keyup", (event) => {
  keys[event.key] = false;
});

// =========================
// ATUALIZA OS JOGADORES
// =========================

function updatePlayers() {
  // Jogador 1
  if (meuJogador === 1) {
    if (keys["w"] || keys["W"]) {
      player1Y -= 6;
    }

    if (keys["s"] || keys["S"]) {
      player1Y += 6;
    }

    player1Y = Math.max(0, Math.min(400, player1Y));

    paddlePlayer1.style.top = `${player1Y}px`;
  }

  // Jogador 2
  if (meuJogador === 2) {
    if (keys["ArrowUp"]) {
      player2Y -= 6;
    }

    if (keys["ArrowDown"]) {
      player2Y += 6;
    }

    player2Y = Math.max(0, Math.min(400, player2Y));

    paddlePlayer2.style.top = `${player2Y}px`;
  }

  // Envia a posição da própria raquete
  if (
    socket.readyState === WebSocket.OPEN &&
    meuJogador !== null &&
    !gameOver
  ) {
    socket.send(
      JSON.stringify({
        tipo: "raquete",
        jogador: meuJogador,
        y: meuJogador === 1 ? player1Y : player2Y,
      }),
    );
  }
}

// =========================
// TELA DE VITÓRIA
// =========================

function mostrarTelaVitoria() {
  gameOver = true;

  let vencedor;

  if (player1Score >= 5) {
    vencedor = "Jogador 1 venceu!";
  } else if (player2Score >= 5) {
    vencedor = "Jogador 2 venceu!";
  }

  winnerMessage.textContent = vencedor;

  finalScore.textContent = `${player1Score} x ${player2Score}`;

  status.textContent = "Fim de jogo!";

  gameOverScreen.style.display = "flex";
}

// =========================
// ESCONDER TELA DE VITÓRIA
// =========================

function esconderTelaVitoria() {
  gameOverScreen.style.display = "none";

  gameOver = false;

  player1Score = 0;
  player2Score = 0;

  scorePlayer1.textContent = "0";
  scorePlayer2.textContent = "0";

  status.textContent = `Você é o Jogador ${meuJogador}`;
}

// =========================
// VERIFICA VENCEDOR
// =========================

function checkWinner() {
  if (player1Score >= 5 || player2Score >= 5) {
    mostrarTelaVitoria();
  }
}

// =========================
// JOGAR NOVAMENTE
// =========================

restartButton.addEventListener("click", () => {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(
      JSON.stringify({
        tipo: "reiniciar",
      }),
    );

    esconderTelaVitoria();
  }
});

// =========================
// LOOP PRINCIPAL
// =========================

function gameLoop() {
  if (!gameOver) {
    updatePlayers();
  }

  requestAnimationFrame(gameLoop);
}

// =========================
// STATUS INICIAL
// =========================

status.textContent = "Conectando ao servidor...";

// =========================
// RECEBE MENSAGENS
// =========================

socket.onmessage = (event) => {
  const mensagem = event.data;

  console.log("Servidor:", mensagem);

  // =========================
  // JOGADOR 1
  // =========================

  if (mensagem === "Você é o jogador 1") {
    meuJogador = 1;

    status.textContent = "Você é o Jogador 1 • W / S";

    return;
  }

  // =========================
  // JOGADOR 2
  // =========================

  if (mensagem === "Você é o jogador 2") {
    meuJogador = 2;

    status.textContent = "Você é o Jogador 2 • ↑ / ↓";

    return;
  }

  // =========================
  // AGUARDANDO JOGADOR
  // =========================

  if (mensagem === "AGUARDANDO") {
    gameOver = true;

    status.textContent = "Aguardando Jogador 2...";

    return;
  }

  // =========================
  // PARTIDA INICIADA
  // =========================

  if (mensagem === "INICIAR_PARTIDA") {
    gameOver = false;

    gameOverScreen.style.display = "none";

    if (meuJogador === 1) {
      status.textContent = "Você é o Jogador 1 • W / S";
    } else {
      status.textContent = "Você é o Jogador 2 • ↑ / ↓";
    }

    return;
  }

  // =========================
  // NOVA PARTIDA
  // =========================

  if (mensagem === "NOVA_PARTIDA") {
    gameOver = false;

    gameOverScreen.style.display = "none";

    if (meuJogador === 1) {
      status.textContent = "Você é o Jogador 1 • W / S";
    } else {
      status.textContent = "Você é o Jogador 2 • ↑ / ↓";
    }

    return;
  }

  // =========================
  // PLACAR
  // =========================

  if (mensagem.startsWith("PLACAR:")) {
    const placar = mensagem.replace("PLACAR:", "").split(",");

    player1Score = Number(placar[0]);

    player2Score = Number(placar[1]);

    scorePlayer1.textContent = player1Score;

    scorePlayer2.textContent = player2Score;

    checkWinner();

    return;
  }

  // =========================
  // RAQUETE
  // =========================

  try {
    const dados = JSON.parse(mensagem);

    if (dados.tipo === "raquete") {
      if (dados.jogador === 1 && meuJogador !== 1) {
        player1Y = dados.y;

        paddlePlayer1.style.top = `${player1Y}px`;
      }

      if (dados.jogador === 2 && meuJogador !== 2) {
        player2Y = dados.y;

        paddlePlayer2.style.top = `${player2Y}px`;
      }

      return;
    }
  } catch (erro) {
    // Mensagem não era JSON
  }

  // =========================
  // BOLA
  // =========================

  if (/^\d+(\.\d+)?,\d+(\.\d+)?$/.test(mensagem)) {
    const [x, y] = mensagem.split(",");

    ballX = Number(x);

    ballY = Number(y);

    ball.style.left = `${ballX}px`;

    ball.style.top = `${ballY}px`;
  }
};

gameLoop();
