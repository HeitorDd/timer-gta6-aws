from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# 19/11/2026 a meia-noite no horario de Brasilia (UTC-3) = 03:00 UTC
LANCAMENTO = datetime(2026, 11, 19, 3, 0, 0, tzinfo=timezone.utc)


@app.get("/health")
def health():
    return {"status": "online", "servico": "ECS Express + ECR"}


@app.get("/api/gta6")
def tempo_restante():
    agora = datetime.now(timezone.utc)
    segundos = max(0, int((LANCAMENTO - agora).total_seconds()))
    return {
        "lancamento": LANCAMENTO.isoformat(),
        "segundos_restantes": segundos,
        "dias": segundos // 86400,
        "horas": (segundos % 86400) // 3600,
        "minutos": (segundos % 3600) // 60,
        "segundos": segundos % 60,
        "lancou": segundos == 0,
    }


PAGINA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Contagem regressiva - GTA VI</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    min-height: 100vh;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    color: #fff;
    background: linear-gradient(160deg, #1a0b2e 0%, #4a1259 45%, #c2185b 80%, #ff8a3d 100%);
    text-align: center; padding: 24px;
  }
  h1 { font-size: clamp(2rem, 6vw, 4rem); letter-spacing: 0.08em; text-shadow: 0 0 24px rgba(255,105,180,.6); }
  .sub { margin-top: 8px; opacity: .85; font-size: clamp(1rem, 2.5vw, 1.25rem); }
  .timer { display: flex; gap: clamp(10px, 3vw, 28px); margin: 40px 0; flex-wrap: wrap; justify-content: center; }
  .bloco {
    background: rgba(0,0,0,.35); border: 1px solid rgba(255,255,255,.2);
    border-radius: 16px; padding: 20px 10px; min-width: clamp(80px, 18vw, 150px);
    backdrop-filter: blur(6px);
  }
  .num { font-size: clamp(2.5rem, 8vw, 5rem); font-weight: 800; font-variant-numeric: tabular-nums; }
  .rot { text-transform: uppercase; letter-spacing: .15em; font-size: .8rem; opacity: .8; margin-top: 6px; }
  .lancou { font-size: clamp(2rem, 6vw, 3.5rem); font-weight: 800; margin: 40px 0; display: none; }
  footer { opacity: .6; font-size: .8rem; }
</style>
</head>
<body>
  <h1>GTA VI</h1>
  <p class="sub">Lan&ccedil;amento: 19 de novembro de 2026 &middot; PS5 e Xbox Series X|S</p>

  <div class="timer" id="timer">
    <div class="bloco"><div class="num" id="d">--</div><div class="rot">dias</div></div>
    <div class="bloco"><div class="num" id="h">--</div><div class="rot">horas</div></div>
    <div class="bloco"><div class="num" id="m">--</div><div class="rot">minutos</div></div>
    <div class="bloco"><div class="num" id="s">--</div><div class="rot">segundos</div></div>
  </div>
  <div class="lancou" id="lancou">J&aacute; lan&ccedil;ou! Vai jogar!</div>

  <footer>Rodando na AWS &middot; ECS Express Mode</footer>

<script>
  const LANCAMENTO = new Date("2026-11-19T03:00:00Z").getTime();
  const dois = n => String(n).padStart(2, "0");

  function atualizar() {
    const resta = Math.max(0, Math.floor((LANCAMENTO - Date.now()) / 1000));
    if (resta === 0) {
      document.getElementById("timer").style.display = "none";
      document.getElementById("lancou").style.display = "block";
      return;
    }
    document.getElementById("d").textContent = Math.floor(resta / 86400);
    document.getElementById("h").textContent = dois(Math.floor((resta % 86400) / 3600));
    document.getElementById("m").textContent = dois(Math.floor((resta % 3600) / 60));
    document.getElementById("s").textContent = dois(resta % 60);
  }
  atualizar();
  setInterval(atualizar, 1000);
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def pagina():
    return PAGINA
