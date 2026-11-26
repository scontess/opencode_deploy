import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import Flask, render_template, request

app = Flask(__name__)

# In locale comodo il reload automatico; su Render imposta FLASK_DEBUG=0.
DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

# I server Render usano UTC: qui si converte nel fuso italiano.
FUSO = os.getenv("APP_TIMEZONE", "Europe/Rome")


def _fuso():
    """ZoneInfo se il database dei fusi è disponibile, altrimenti UTC."""
    try:
        return ZoneInfo(FUSO)
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def _indirizzo() -> str:
    """URL pubblico reale, anche dietro il proxy di Render/Cloudflare."""
    schema = request.headers.get("X-Forwarded-Proto", request.scheme)
    return f"{schema}://{request.host}"


@app.get("/")
def index():
    adesso = datetime.now(_fuso())
    return render_template(
        "index.html",
        giorno=adesso.strftime("%d/%m/%Y"),
        ora=adesso.strftime("%H:%M:%S"),
        fuso=FUSO,
        indirizzo=_indirizzo(),
    )


@app.get("/health")
def health():
    """Usato da Render e dai controlli di uptime."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=DEBUG)
