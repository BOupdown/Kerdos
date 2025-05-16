import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app, resources={r"/calculs/*": {"origins": "*"}})

calculs_bp = Blueprint("calculs", __name__)
# Configuration de la connexion à la base de données

password = os.getenv("MYSQL_ROOT_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database=database,
            port=4306,
            connection_timeout=60  # Timeout de 60 secondes
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
        return None

# Route pour récupérer toutes les formules (GET)
@calculs_bp.route("/formules", methods=["GET", "OPTIONS"])
@cross_origin(origins="*")
def get_formules():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM formules")
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(results)

# Route pour ajouter une nouvelle formule (POST)
@calculs_bp.route("/formules", methods=["POST", "OPTIONS"])
@cross_origin(origins="*")
def add_formule():
    data = request.json
    name = data.get('name')
    formula = data.get('formula')

    if not name or not formula:
        return jsonify({"error": "Nom et formule sont requis"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    cursor = conn.cursor()
    sql = "INSERT INTO formules (name, formula) VALUES (%s, %s)"
    cursor.execute(sql, (name, formula))
    conn.commit()
    
    inserted_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"id": inserted_id, "name": name, "formula": formula}), 201

# Route pour récupérer toutes les variables (GET)
@calculs_bp.route("/variables", methods=["GET", "OPTIONS"])
@cross_origin(origins="*")
def get_variables():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM variables")
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(results)

@calculs_bp.route("/variables", methods=["POST", "OPTIONS"])
@cross_origin(origins="*")
def add_variable():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Nom est requis"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Impossible de se connecter à la base de données"}), 500

    cursor = conn.cursor()
    sql = "INSERT INTO variables (name) VALUES (%s)"
    cursor.execute(sql, (name,))
    conn.commit()

    inserted_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"id": inserted_id, "name": name}), 201

app.register_blueprint(calculs_bp, url_prefix="/calculs")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)