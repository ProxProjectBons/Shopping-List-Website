import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS allows your browser to send data from the website to the Python backend
CORS(app)

DB_NAME = "shopping_list.db"

def init_db():
    """Creates the database and the table for the shopping list."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()

@app.route('/', methods=['GET'])
def index():
    """Home page to show that the backend is running."""
    return jsonify({
        "status": "Online",
        "message": "Das Shopping-List Backend läuft! Nutze /api/items für die Liste."
    })

@app.route('/api/scan', methods=['POST'])
def save_scan():
    """Saves a scanned value."""
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Daten unvollständig"}), 400

    content = data['content']
    print(f"DEBUG: Empfangener Scan: {content}") # Shows in console what was scanned

    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items (content) VALUES (?)", (content,))
        connection.commit()
        item_id = cursor.lastrowid
        connection.close()
        print(f"DEBUG: Erfolgreich in DB gespeichert mit ID: {item_id}")
        return jsonify({"message": "Gespeichert", "id": item_id, "content": content}), 201
    except Exception as e:
        print(f"DEBUG: Fehler beim Speichern: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/items', methods=['GET'])
def get_items():
    """Loads all entries from the database."""
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT id, content, timestamp FROM items ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        connection.close()
        
        items = [{"id": r[0], "content": r[1], "timestamp": r[2]} for r in rows]
        print(f"DEBUG: {len(items)} Items an Frontend gesendet")
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Deletes a product."""
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        connection.commit()
        connection.close()
        print(f"DEBUG: Item mit ID {item_id} gelöscht")
        return jsonify({"message": "Gelöscht"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    # Runs the server on port 5000
    app.run(debug=True, port=5000)