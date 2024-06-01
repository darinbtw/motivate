from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from routes import auth, user

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
