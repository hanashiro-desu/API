from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'db.json'

# Load hoặc khởi tạo dữ liệu
if os.path.exists(DB_PATH):
    with open(DB_PATH, encoding='utf-8') as f:
        db = json.load(f)
else:
    db = {"notes": [], "accounts": []}

def save_db():
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    return jsonify({'message': 'Đây là Web của Shiori-desu'})

# ──────────────── Notes ────────────────

@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(db['notes'])

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = next((n for n in db['notes'] if n['id'] == note_id), None)
    if note:
        return jsonify(note)
    return jsonify({'error': 'Note not found'}), 404

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    data['id'] = max([n['id'] for n in db['notes']] or [0]) + 1
    db['notes'].append(data)
    save_db()
    return jsonify(data), 201

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    for i, note in enumerate(db['notes']):
        if note['id'] == note_id:
            data['id'] = note_id
            db['notes'][i] = data
            save_db()
            return jsonify(data)
    return jsonify({'error': 'Note not found'}), 404

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    for i, note in enumerate(db['notes']):
        if note['id'] == note_id:
            del db['notes'][i]
            save_db()
            return jsonify({'message': 'Note deleted'})
    return jsonify({'error': 'Note not found'}), 404

# ──────────────── Accounts ────────────────

@app.route('/accounts', methods=['GET'])
def get_accounts():
    return jsonify(db['accounts'])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = next((u for u in db['accounts'] if u['username'] == username and u['password'] == password), None)
    if user:
        return jsonify({'message': 'Login successful', 'userId': user['userId']})
    return jsonify({'error': 'Invalid credentials'}), 401

# ──────────────── Run ────────────────

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
