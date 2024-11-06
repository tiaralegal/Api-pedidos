from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/middlend/menu', methods=['GET'])
def obtener_menu():
    try:
        response = requests.get('http://127.0.0.1:5000/menu')
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "No se pudo obtener el menú"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/middlend/pedido', methods=['GET'])
def obtener_orden_api():
    try:
        response = requests.get("http://127.0.0.1:5000/pedido")
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "No se pudo obtener el pedido"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/middlend/inventario', methods=['GET'])
def obtener_inventario_api():
    try:
        response = requests.get("http://127.0.0.1:5000/inventario")
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "No se pudo obtener el inventario"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)



    
