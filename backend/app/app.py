import os
import json
import urllib.request
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, DDL, Column, Integer, String, Numeric, DateTime, func, Enum, ForeignKey
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://administrador:Ld8vp14eh4UdF6H9YpN5bkHe5CzjUkqv@dpg-cq1pbs2ju9rs73bbo3p0-a.oregon-postgres.render.com/ferremas_ersz'
db = SQLAlchemy(app)

@app.route("/flask", methods=['GET'])
def index():
    return "Flask server"

class Venta(db.Model):
    __tablename__ = 'venta'
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    inventarios = db.relationship('Inventario', backref=db.backref('producto', lazy=True))
    historial_precios = db.relationship('HistorialPrecioProducto', backref='producto', lazy=True)

class HistorialPrecioProducto(db.Model):
    __tablename__ = 'historial_precios_producto'
    id_historial_precio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    precio_anterior = db.Column(db.Numeric(10, 2), nullable=False)
    precio_nuevo = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_modificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id_inventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id_sucursal'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, nombre):
        self.nombre = nombre

class Sucursal(db.Model):
    __tablename__ = 'sucursal'
    id_sucursal = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    inventarios = db.relationship('Inventario', backref='sucursal', lazy=True)
    vendedores = db.relationship('Vendedor', backref='sucursal', lazy=True)

class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    id_vendedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id_sucursal'))

class Chat(db.Model):
    __tablename__ = 'chat'
    id_mensaje = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensaje = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    id_chat = db.Column(db.Numeric(10, 2), nullable=False)


class Promocion(db.Model):
    __tablename__ = 'promocion'

    id_promocion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, ForeignKey('producto.id_producto'), nullable=False)
    tipo_promocion = db.Column(db.Enum('promocion', 'lanzamiento',name='tipo_promocion_enum'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)


class TasaCambio(db.Model):
    __tablename__ = 'tasas_cambio'
    moneda_destino = Column(String(3), primary_key=True)
    tasa = Column(Numeric(18, 6), nullable=False)
    fecha_actualizacion = Column(DateTime, default=func.now(), nullable=False)

def obtener_tasas_desde_api():
    api_url = 'https://api.exchangerate-api.com/v4/latest/CLP' 
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read())
            tasas = data['rates']
            return tasas
    except Exception as e:
        print(f"Error al obtener las tasas de cambio desde la API: {e}")
        return None

def actualizar_tasas_cambio():
    tasas = obtener_tasas_desde_api()
    try:
        if tasas:
            for moneda, tasa in tasas.items():
                tasa_cambio = TasaCambio.query.filter_by(moneda_destino=moneda).first()
                if tasa_cambio:
                    tasa_cambio.tasa = tasa
                else:
                    tasa_cambio = TasaCambio(moneda_destino=moneda, tasa=tasa)
                    db.session.add(tasa_cambio)
            
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al actualizar las tasas de cambio: {e}")
        db.session.rollback()
        return False

@app.route('/actualizar-tasas-cambio', methods=['GET'])
def ruta_actualizar_tasas_cambio():
    if actualizar_tasas_cambio():
        return jsonify({'message': 'Tasas de cambio actualizadas correctamente.'}), 200
    else:
        return jsonify({'message': 'Error al actualizar las tasas de cambio.'}), 500