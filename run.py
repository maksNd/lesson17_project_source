from app_config.config import api
from flask import current_app
from data_manager.create_data import fill_db

app = current_app

if __name__ == '__main__':
    fill_db()
    app.run(debug=True)
