import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://administrador:Ld8vp14eh4UdF6H9YpN5bkHe5CzjUkqv@dpg-cq1pbs2ju9rs73bbo3p0-a.oregon-postgres.render.com/ferremas_ersz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clavesecreta'
