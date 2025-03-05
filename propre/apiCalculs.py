from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Active CORS

# Configuration de la connexion à la base de données
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="omarleboss",
            database="Calculs",
            port=4306,
            connection_timeout=60  # Timeout de 60 secondes
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
        return None

# Route pour récupérer toutes les formules (GET)
@app.route('/formules', methods=['GET'])
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
@app.route('/formules', methods=['POST'])
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
@app.route('/variables', methods=['GET'])
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

# Route pour ajouter une nouvelle variable (POST)
@app.route('/variables', methods=['POST'])
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

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(port=3000, debug=False)
