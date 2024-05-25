from .models import *
def serialize_cliente(cliente):
    return {
        'id_cliente': cliente.id_cliente,
        'seleccionar_producto': cliente.seleccionar_producto,
        'solicitar_producto': cliente.solicitar_producto,
        'reclamar_producto': cliente.reclamar_producto,
        'recibir_producto': cliente.recibir_producto
    }

def serialize_contador(contador):
    return {
        'id_contador': contador.id_contador,
        'registrar_entrega': contador.registrar_entrega,
        'registrar_pago': contador.registrar_pago
    }

def serialize_venta(detalle_producto):
    return {
        'id_detalle_producto': detalle_producto.id_detalle_producto,
        'precio': float(detalle_producto.precio),  # Convertir a float para la serialización JSON
        'cantidad': detalle_producto.cantidad
    }

def serialize_encargado(encargado):
    return {
        'id_encargado': encargado.id_encargado,
        'checar_producto': encargado.checar_producto,
        'informar_al_cierre': encargado.informar_al_cierre,
        'recibir_pago': encargado.recibir_pago,
        'recibir_producto': encargado.recibir_producto
    }

def serialize_ferramax(ferramax):
    return {
        'id_ferramax': ferramax.id_ferramax
    }

def serialize_producto(producto):
    return {
        'id_producto': producto.id_producto,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'precio': float(producto.precio),  # Convertir a float para la serialización JSON
        'stock': producto.stock,
        'fecha_creacion': producto.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
    }

def serialize_webpay(webpay):
    return {
        'id_webpay': webpay.id_webpay
    }
