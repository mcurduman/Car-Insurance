from flask import Flask
import logging
from app.core.settings import get_settings

def create_app() -> Flask:
    cfg = get_settings()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-me"  # sau cfg din env dacă vrei

    logging.basicConfig(level=getattr(logging, cfg.LOG_LEVEL),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    # init extensii aici (db, etc.)
    return app