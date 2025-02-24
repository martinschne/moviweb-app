from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/moviweb_app.db"

db = SQLAlchemy(app)

data_manager = SQLiteDataManager(db)

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string


if __name__ == "__main__":
    app.run(debug=True)