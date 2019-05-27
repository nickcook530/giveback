from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

#initiatlize app
app = Flask(__name__)
app.config.from_object(Config)

#initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

#imports at bottom to avoid circular imports
from mypackage import routes, models