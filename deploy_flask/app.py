import os
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)

# In locale comodo il reload automatico; su Render imposta FLASK_DEBUG=0.
DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"


@app.get("/")
def index():
    return render_template(
        "index.html",
        ora=datetime.now().strftime("%H:%M:%S"),
        giorno=datetime.now().strftime("%d/%m/%Y"),
    )


@app.get("/health")
def health():
    """Usato da Render e dai controlli di uptime."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=DEBUG)
