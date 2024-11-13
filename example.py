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
  pedidos = cursor.fetchall()
  print(pedidos)
  if pedidos :
    json_return = [{'id': pedido[0], 'stock': pedido[1], 'precio':pedido[2], 'descripcion':pedido[3]} for pedido in pedidos]
    return jsonify(json_return)
  return jsonify({'message': 'Pedido no encontrado'}), 404

@app.route('/pedido', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    fecha = data.get('fecha')
    estado_id = data.get('Estado_idEstado')
    detalles = data.get('detalles')  # Lista de detalles [{ "articulos_id": 1, "cantidad": 2, "precio_unitario": 10.5 }, ...]

    if not fecha or not estado_id or not detalles:
        return jsonify({'message': 'Datos incompletos'}), 400

    cursor = mydb.cursor()
    # Insertar en la tabla pedido
    cursor.execute("INSERT INTO pedido (fecha, Estado_idEstado) VALUES (%s, %s) RETURNING idPedido", (fecha, estado_id))
    pedido_id = cursor.fetchone()[0]

    # Insertar en la tabla pedido_detalle para cada artículo
    for detalle in detalles:
        cursor.execute(
            "INSERT INTO pedido_detalle (articulos_idarticulos, Pedido_idPedido, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
            (detalle['articulos_id'], pedido_id, detalle['cantidad'], detalle['precio_unitario'])
        )
  
    mydb.commit()
    return jsonify({'message': 'Pedido creado', 'pedido_id': pedido_id}), 201


@app.route('/pedido/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    data = request.get_json()
    fecha = data.get('fecha')
    estado_id = data.get('Estado_idEstado')
    detalles = data.get('detalles')

    cursor = mydb.cursor()
    # Actualizar la tabla pedido
    cursor.execute("UPDATE pedido SET fecha = %s, Estado_idEstado = %s WHERE idPedido = %s", (fecha, estado_id, id))

    # Actualizar detalles del pedido (borramos y volvemos a insertar para simplificar)
    cursor.execute("DELETE FROM pedido_detalle WHERE Pedido_idPedido = %s", (id,))
    for detalle in detalles:
        cursor.execute(
            "INSERT INTO pedido_detalle (articulos_idarticulos, Pedido_idPedido, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
            (detalle['articulos_id'], id, detalle['cantidad'], detalle['precio_unitario'])
        )
  
    mydb.commit()
    return jsonify({'message': 'Pedido actualizado'})



@app.route('/pedido/<int:id>', methods=['DELETE'])
def eliminar_pedido(id):
    cursor = mydb.cursor()
    # Eliminar detalles asociados al pedido
    cursor.execute("DELETE FROM pedido_detalle WHERE Pedido_idPedido = %s", (id,))
    # Eliminar el pedido en sí
    cursor.execute("DELETE FROM pedido WHERE idPedido = %s", (id,))
  
    mydb.commit()
    return jsonify({'message': 'Pedido eliminado'})



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
