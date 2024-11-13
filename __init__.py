from flask import Flask
from app.routes import posts  # Importamos el blueprint de posts
from app.utils.db import db  # Importamos la conexión a MySQL

def create_app():
    app = Flask(_name_)
    app.config.from_object('app.config.Config')  # Cargamos la configuración

    # Inicializamos la conexión a MongoDB
    db.init_app(app)

    # Registramos el blueprint de posts
    app.register_blueprint(posts.bp)

    return app