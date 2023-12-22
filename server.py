from app.routes import app

if __name__ == '__main__':
    app.run(port=app.config['FLASK_RUN_PORT'], load_dotenv=True)
