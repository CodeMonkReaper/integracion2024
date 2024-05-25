import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://administrador:NCPgatauFcE4HfYylftN8tX7YAyfNbSv@dpg-cp74hngl6cac7386tmmg-a.oregon-postgres.render.com/ferremas_6a85'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clavesecreta'
