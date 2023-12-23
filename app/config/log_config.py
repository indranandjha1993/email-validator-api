import logging
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    logging.basicConfig(level=logging.INFO)

    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
