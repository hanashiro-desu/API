from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # ✅ gọi CORS sau khi app được khởi tạo

# Load dữ liệu từ db.json
with open('db.json', encoding='utf-8') as f:
    db = json.load(f)

@app.route('/')
def home():
    return jsonify({'message': 'Đây là Web của Shiori-desu'})

@app.route('/notes')
def get_notes():
    return jsonify(db['notes'])

@app.route('/accounts')
def get_accounts():
    return jsonify(db['accounts'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
