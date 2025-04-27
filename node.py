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
    for account in db['accounts']:
        account.setdefault('status', 'active')
    return jsonify(db['accounts'])

@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account_by_id(account_id):
    account = next((a for a in db['accounts'] if a.get('id') == account_id), None)
    if account:
        return jsonify(account)
    return jsonify({'error': 'Account not found'}), 404

@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    data['id'] = max([a['id'] for a in db['accounts']] or [0]) + 1
    data.setdefault('status', 'active')
    db['accounts'].append(data)
    save_db()
    return jsonify(data), 201

@app.route('/accounts/<int:account_id>', methods=['PATCH'])
def patch_account(account_id):
    data = request.get_json()
    account = next((a for a in db['accounts'] if a['id'] == account_id), None)
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    account.update(data)
    save_db()
    return jsonify(account)

@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.get_json()
    for i, acc in enumerate(db['accounts']):
        if acc['id'] == account_id:
            data['id'] = account_id
            db['accounts'][i] = data
            save_db()
            return jsonify(data)
    return jsonify({'error': 'Account not found'}), 404

@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    for i, acc in enumerate(db['accounts']):
        if acc['id'] == account_id:
            del db['accounts'][i]
            save_db()
            return jsonify({'message': 'Account deleted'})
    return jsonify({'error': 'Account not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = next(
        (u for u in db['accounts']
         if u.get('username') == username and
            u.get('password') == password and
            u.get('status', 'active') == 'active'),
        None
    )
    if user:
        return jsonify({'message': 'Login successful', 'id': user.get('id'), 'username': user['username']})
    return jsonify({'error': 'Invalid credentials'}), 401

# ──────────────── Run ────────────────

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
