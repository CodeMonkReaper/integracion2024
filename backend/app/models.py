from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

    def __init__(self, nombre, email, password, rol_id):
        self.nombre = nombre
        self.email = email
        self.set_password(password)
        self.rol_id = rol_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Venta(db.Model):
    __tablename__ = 'venta'
    id_venta = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)


class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True)
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
    id_historial_precio = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    precio_anterior = db.Column(db.Numeric(10, 2), nullable=False)
    precio_nuevo = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_modificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Inventario(db.Model):
    __tablename__ = 'inventario'

    id_inventario = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id_sucursal'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

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

class Rol(db.Model):
    __tablename__ = 'rol'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, nombre):
        self.nombre = nombre

class Vendedor(db.Model):
    __tablename__ = 'vendedor'

    id_vendedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id_sucursal'))

    def __init__(self, nombre, email, password, rol_id):
        self.nombre = nombre
        self.email = email
        self.set_password(password)
        self.rol_id = rol_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
