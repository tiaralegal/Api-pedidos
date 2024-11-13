# Ejemplo API Pedidos

from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la base de datos
mydb = psycopg2.connect(
  host="dpg-cslunk9u0jms73b9b7og-a.oregon-postgres.render.com",
  user="pedidos_db_wdti_user",
  password="Z0UQkivVcoh0MucJX4YZKfuh4zOmGUEp",
  database="pedidos_db_wdti"
)


@app.route('/pedido', methods=['GET'])
def obtener_pedido():
  cursor = mydb.cursor()
  cursor.execute("SELECT * FROM articulos ")
  pedidos = cursor.fetchone()
  if pedidos :
    json_return = [{'id': pedido[1], 'stock': pedido[2], 'precio':pedido[3], 'descripcion':pedido[4]} for pedido in pedidos]
    return jsonify(json_return)
  return jsonify({'message': 'Pedido no encontrado'}), 404

@app.route('/pedido', methods=['POST'])
def crear_pedido():
  # Obtener los datos del pedido desde la solicitud
  # ...
  cursor = mydb.cursor()
  # Insertar el pedido en la base de datos
  # ...
  mydb.commit()
  return jsonify({'message': 'Pedido creado'}), 201

@app.route('/pedido', methods=['PUT'])
def actualizar_pedido(id):
  # Obtener los datos del pedido desde la solicitud
  # ...
  cursor = mydb.cursor()
  # Actualizar el pedido en la base de datos
  # ...
  mydb.commit()
  return jsonify({'message': 'Pedido actualizado'})

@app.route('/pedido', methods=['DELETE'])
def eliminar_pedido(id):
  cursor = mydb.cursor()
  # Eliminar el pedido de la base de datos
  # ...
  mydb.commit()
  return jsonify({'message': 'Pedido eliminado'})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
