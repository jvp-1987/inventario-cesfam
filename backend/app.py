from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Configuración básica
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False)

# Ruta para ver productos
@app.route("/productos", methods=["GET"])
def obtener_productos():
    productos = Producto.query.all()
    resultado = []
    for p in Productos:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "categoria": p.categoria,
            "stock": p.stock,
            "stock_minimo": p.stock_minimo
        })
    return jsonify(resultado)
# Ruta eliminar
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado"}), 200
# Ruta edeitar
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.get_json()
    Producto = Producto.query.get_or_404(id)
    Producto.nombre = data["nombre"]
    Producto.categoria = data["categoria"]
    Producto.stock = data["stock"]
    Producto.stock_minimo = data["stock_minimo"]
    db.session.commit()
    return jsonify({"mensaje": "Producto actualizado"})
# Ejecutar al iniciar la app
if __name__ == "__main__":
    with app.app_context():
        # Crear base de datos
        db.create_all()

        # Insertar productos si está vacía
        if Producto.query.count() == 0:
            productos = [
                Producto(nombre="Jabón líquido", categoria="Aseo", stock=20, stock_minimo=5),
                Producto(nombre="Papel higiénico", categoria="Aseo", stock=50, stock_minimo=10),
                Producto(nombre="Lapiceros", categoria="Escritorio", stock=100, stock_minimo=20),
                Producto(nombre="Cuadernos", categoria="Escritorio", stock=80, stock_minimo=15),
                Producto(nombre="Toner impresora", categoria="Imprenta", stock=10, stock_minimo=5),
            ]
            db.session.bulk_save_objects(productos)
            db.session.commit()
            print("✅ Productos cargados en la base de datos")

    app.run(debug=True, port=5001)


