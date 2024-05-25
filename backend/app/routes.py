from flask import Blueprint, request, jsonify,render_template,Flask
from .models import db, Cliente,Producto,Venta,Vendedor,Sucursal
from .serializer import serialize_cliente,serialize_producto,serialize_venta
from datetime import datetime
from functools import wraps
from flask import abort
from flask_login import current_user
from flask_bcrypt import check_password_hash
import jwt


main=Blueprint('main',__name__)
def init_routes(app):
    app.register_blueprint(main)
def vendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.has_role('vendedor'):
            return f(*args, **kwargs)
        else:
            abort(403)  # Forbidden
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.has_role('admin'):
            return f(*args, **kwargs)
        else:
            abort(403)  # Forbidden
    return decorated_function


#login cliente
@main.route('/cliente/register', methods=['POST'])
def register_cliente():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    rol_id = data.get('rol_id')  # Asegúrate de proporcionar también el rol_id

    # Verificar si el cliente ya está registrado
    cliente_existente = Cliente.query.filter_by(email=email).first()
    if cliente_existente:
        return jsonify({"message": "El cliente ya está registrado"}), 400

    # Crear un nuevo cliente
    nuevo_cliente = Cliente(nombre=nombre, email=email, password=password, rol_id=rol_id)
    db.session.add(nuevo_cliente)
    db.session.commit()

    return jsonify({"message": "Cliente registrado exitosamente"}), 201


# Inicio de sesión de cliente
@main.route('/cliente/login', methods=['POST'])
def login_cliente():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cliente = Cliente.query.filter_by(email=email).first()

    if cliente and check_password_hash(cliente.password_hash, password):
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401


#venta
# Función para crear una nueva venta (operación CRUD - Create)
@vendedor_required
def create_venta(data):

    nueva_venta = Venta(
        precio=data.get('precio'),
        cantidad=data.get('cantidad')
    )
    db.session.add(nueva_venta)
    db.session.commit()

# Función para obtener una venta por su ID (operación CRUD - Read)
def get_venta_by_id(venta_id):
    venta = Venta.query.get(venta_id)
    return venta

# Función para actualizar una venta (operación CRUD - Update)
@vendedor_required
def update_venta(venta_id, data):
    venta = Venta.query.get(venta_id)
    venta.precio = data.get('precio', venta.precio)
    venta.cantidad = data.get('cantidad', venta.cantidad)
    db.session.commit()

# Función para eliminar una venta (operación CRUD - Delete)
@vendedor_required
def delete_venta(venta_id):
    venta = Venta.query.get(venta_id)
    db.session.delete(venta)
    db.session.commit()






# Crear un producto
@main.route('/producto/crear', methods=['POST'])
@vendedor_required
def crear_producto():
    data = request.json
    nuevo_producto = Producto(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        precio=data.get('precio'),
        stock=data.get('stock'),
        categoria=data.get('categoria'),
        fecha_creacion=datetime.utcnow()
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({"message": "Producto creado exitosamente"}), 201

# Obtener todos los productos
@main.route('/listarproducto', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    resultados = [serialize_producto(producto) for producto in productos]
    return jsonify(resultados)

# Obtener un producto por su ID
@main.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(serialize_producto(producto))

# Actualizar un producto
@main.route('/producto/<int:id>', methods=['PUT'])
@vendedor_required
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.json
    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    producto.categoria = data.get('categoria', producto.categoria)
    db.session.commit()
    return jsonify({"message": "Producto actualizado exitosamente"})

# Eliminar un producto
@main.route('/producto/<int:id>', methods=['DELETE'])
@vendedor_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "Producto eliminado exitosamente"})







# Registro de un vendedor
@main.route('/vendedor/registro', methods=['POST'])
def register_vendedor():
    data = request.json
    nuevo_vendedor = Vendedor(
        nombre=data.get('nombre'),
        email=data.get('email'),
        password=data.get('password'),  # Asegúrate de que el frontend envíe 'password'
        rol_id=data.get('rol_id'),  # Asegúrate de proporcionar el rol_id
    )
    db.session.add(nuevo_vendedor)
    db.session.commit()
    return jsonify({"message": "Vendedor registrado exitosamente"}), 201

# Inicio de sesión de un vendedor
@main.route('/vendedor/login', methods=['POST'])
def login_vendedor():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    vendedor = Vendedor.query.filter_by(email=email).first()

    if vendedor and check_password_hash(vendedor.password_hash, password):
        # Generar token de sesión
        token = jwt.encode({
            'vendedor_id': vendedor.id_vendedor,
        }, 'secret_key', algorithm='HS256')

        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401






@main.route('/sucursal/crear', methods=['POST'])
def crear_sucursal():
    data = request.json
    nueva_sucursal = Sucursal(
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        ciudad=data.get('ciudad'),
        provincia=data.get('provincia'),
        pais=data.get('pais'),
        telefono=data.get('telefono'),
        email=data.get('email')
    )
    db.session.add(nueva_sucursal)
    db.session.commit()
    return jsonify({"message": "Sucursal creada exitosamente"}), 201

# Obtener todas las sucursales
@main.route('/sucursal', methods=['GET'])
def obtener_sucursales():
    sucursales = Sucursal.query.all()
    resultados = []
    for sucursal in sucursales:
        resultados.append({
            "id_sucursal": sucursal.id_sucursal,
            "nombre": sucursal.nombre,
            "direccion": sucursal.direccion,
            "ciudad": sucursal.ciudad,
            "provincia": sucursal.provincia,
            "pais": sucursal.pais,
            "telefono": sucursal.telefono,
            "email": sucursal.email
        })
    return jsonify(resultados)

# Obtener una sucursal por su ID
@main.route('/sucursal/<int:id>', methods=['GET'])
def obtener_sucursal(id):
    sucursal = Sucursal.query.get_or_404(id)
    return jsonify({
        "id_sucursal": sucursal.id_sucursal,
        "nombre": sucursal.nombre,
        "direccion": sucursal.direccion,
        "ciudad": sucursal.ciudad,
        "provincia": sucursal.provincia,
        "pais": sucursal.pais,
        "telefono": sucursal.telefono,
        "email": sucursal.email
    })

# Actualizar una sucursal
@main.route('/sucursal/<int:id>', methods=['PUT'])
def actualizar_sucursal(id):
    sucursal = Sucursal.query.get_or_404(id)
    data = request.json
    sucursal.nombre = data.get('nombre', sucursal.nombre)
    sucursal.direccion = data.get('direccion', sucursal.direccion)
    sucursal.ciudad = data.get('ciudad', sucursal.ciudad)
    sucursal.provincia = data.get('provincia', sucursal.provincia)
    sucursal.pais = data.get('pais', sucursal.pais)
    sucursal.telefono = data.get('telefono', sucursal.telefono)
    sucursal.email = data.get('email', sucursal.email)
    db.session.commit()
    return jsonify({"message": "Sucursal actualizada exitosamente"})

# Eliminar una sucursal
@main.route('/sucursal/<int:id>', methods=['DELETE'])
def eliminar_sucursal(id):
    sucursal = Sucursal.query.get_or_404(id)
    db.session.delete(sucursal)
    db.session.commit()
    return jsonify({"message": "Sucursal eliminada exitosamente"})





