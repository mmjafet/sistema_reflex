import reflex as rx

# Estado de la aplicación
class State(rx.State):
    # Lista de productos e inventario
    productos = [
        {"id": 1, "nombre": "Producto A", "precio": 10.0, "stock": 20},
        {"id": 2, "nombre": "Producto B", "precio": 15.0, "stock": 10},
    ]
    ventas = []

    # Método para agregar un nuevo producto
    @staticmethod
    def agregar_producto(nombre, precio, stock):
        nuevo_producto = {
            "id": len(State.productos) + 1,
            "nombre": nombre,
            "precio": float(precio),
            "stock": int(stock),
        }
        State.productos.append(nuevo_producto)

    # Método para registrar una venta
    @staticmethod
    def registrar_venta(producto_id, cantidad):
        for producto in State.productos:
            if producto["id"] == producto_id:
                if producto["stock"] >= cantidad:
                    producto["stock"] -= cantidad
                    venta = {
                        "producto": producto["nombre"],
                        "cantidad": cantidad,
                        "total": cantidad * producto["precio"],
                    }
                    State.ventas.append(venta)

# Componentes del sistema
def agregar_producto_form():
    """Formulario para agregar un producto."""
    return rx.vstack(
        rx.heading("Agregar Producto"),
        rx.input(placeholder="Nombre del producto", id="nombre"),
        rx.input(placeholder="Precio", id="precio"),
        rx.input(placeholder="Stock", id="stock"),
        rx.button(
            "Guardar Producto",
            on_click=lambda: State.agregar_producto(
                rx.get_value("nombre"),
                rx.get_value("precio"),
                rx.get_value("stock"),
            ),
        ),
        rx.divider(),
    )

def mostrar_inventario():
    """Tabla que muestra el inventario actual."""
    return rx.vstack(
        rx.heading("Inventario"),
        rx.table(
            rx.tr(
                rx.th("ID"), rx.th("Nombre"), rx.th("Precio"), rx.th("Stock")
            ),
            *[
                rx.tr(
                    rx.td(str(p["id"])),
                    rx.td(p["nombre"]),
                    rx.td(f"${p['precio']:.2f}"),
                    rx.td(str(p["stock"])),
                )
                for p in State.productos
            ],
        ),
    )

def registrar_venta_form():
    """Formulario para registrar una venta."""
    return rx.vstack(
        rx.heading("Registrar Venta"),
        rx.input(placeholder="ID del producto", id="producto_id"),
        rx.input(placeholder="Cantidad", id="cantidad"),
        rx.button(
            "Registrar Venta",
            on_click=lambda: State.registrar_venta(
                int(rx.get_value("producto_id")),
                int(rx.get_value("cantidad")),
            ),
        ),
        rx.divider(),
    )

def mostrar_ventas():
    """Tabla que muestra las ventas realizadas."""
    return rx.vstack(
        rx.heading("Ventas"),
        rx.table(
            rx.tr(
                rx.th("Producto"), rx.th("Cantidad"), rx.th("Total")
            ),
            *[
                rx.tr(
                    rx.td(v["producto"]),
                    rx.td(str(v["cantidad"])),
                    rx.td(f"${v['total']:.2f}"),
                )
                for v in State.ventas
            ],
        ),
    )

# Interfaz principal
def app():
    return rx.vstack(
        agregar_producto_form(),
        mostrar_inventario(),
        registrar_venta_form(),
        mostrar_ventas(),
    )
