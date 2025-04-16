from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'db.json'

# Load dữ liệu từ db.json hoặc khởi tạo rỗng nếu chưa có
if os.path.exists(DB_PATH):
    with open(DB_PATH, encoding='utf-8') as f:
        db = json.load(f)
else:
    db = {"notes": [], "accounts": []}

# Ghi dữ liệu vào db.json
def save_db():
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

# Trang chủ
@app.route('/')
def home():
    return jsonify({'message': 'Đây là Web của Shiori-desu'})

# ──────────────── Notes API ────────────────

# Lấy tất cả ghi chú
@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(db['notes'])

# Lấy ghi chú theo ID
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = next((n for n in db['notes'] if n['id'] == note_id), None)
    if note:
        return jsonify(note)
    return jsonify({'error': 'Note not found'}), 404

# Thêm ghi chú mới
@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    # Tự động tạo ID
    data['id'] = (max([n['id'] for n in db['notes']] or [0]) + 1)
    db['notes'].append(data)
    save_db()
    return jsonify(data), 201

# Cập nhật ghi chú
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    for i, note in enumerate(db['notes']):
        if note['id'] == note_id:
            data['id'] = note_id  # Đảm bảo ID không bị thay đổi
            db['notes'][i] = data
            save_db()
            return jsonify(data)
    return jsonify({'error': 'Note not found'}), 404

# Xoá ghi chú
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    for i, note in enumerate(db['notes']):
        if note['id'] == note_id:
            del db['notes'][i]
            save_db()
            return jsonify({'message': 'Note deleted'})
    return jsonify({'error': 'Note not found'}), 404

# ──────────────── Accounts API ────────────────

@app.route('/accounts', methods=['GET'])
def get_accounts():
    return jsonify(db['accounts'])

# ──────────────── Run App ────────────────

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
