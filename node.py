from flask import Flask, jsonify, request  # Import các module cần thiết từ Flask để tạo API
from flask_cors import CORS  # Để hỗ trợ CORS (Cross-Origin Resource Sharing), cho phép các request từ domain khác
import json  # Để làm việc với dữ liệu JSON
import os  # Để thao tác với hệ thống tệp, kiểm tra sự tồn tại của file

app = Flask(__name__)  # Tạo một ứng dụng Flask mới
CORS(app)  # Bật CORS cho ứng dụng, cho phép giao tiếp giữa các miền khác nhau

DB_PATH = 'db.json'  # Định nghĩa đường dẫn tới tệp dữ liệu (file db.json)

# Kiểm tra nếu file db.json tồn tại, nếu có thì load dữ liệu, nếu không thì tạo dữ liệu mặc định
if os.path.exists(DB_PATH):
    with open(DB_PATH, encoding='utf-8') as f:  # Mở file db.json để đọc
        db = json.load(f)  # Đọc dữ liệu từ file và lưu vào biến db
else:
    db = {"notes": [], "accounts": []}  # Nếu không có file thì khởi tạo dữ liệu mặc định

# Hàm để lưu dữ liệu vào file db.json
def save_db():
    with open(DB_PATH, 'w', encoding='utf-8') as f:  # Mở file db.json để ghi
        json.dump(db, f, ensure_ascii=False, indent=2)  # Ghi dữ liệu db vào file, định dạng đẹp

@app.route('/')  # Định nghĩa route cho trang chủ
def home():
    return jsonify({'message': 'Đây là Web của Shiori-desu'})  # Trả về một thông điệp JSON

# ──────────────── Notes ────────────────

@app.route('/notes', methods=['GET'])  # Route để lấy tất cả các ghi chú (GET)
def get_notes():
    return jsonify(db['notes'])  # Trả về tất cả các ghi chú từ db dưới dạng JSON

@app.route('/notes/<int:note_id>', methods=['GET'])  # Route để lấy một ghi chú theo ID (GET)
def get_note(note_id):
    note = next((n for n in db['notes'] if n['id'] == note_id), None)  # Tìm ghi chú có ID trùng khớp
    if note:
        return jsonify(note)  # Nếu tìm thấy, trả về ghi chú dưới dạng JSON
    return jsonify({'error': 'Note not found'}), 404  # Nếu không tìm thấy, trả về lỗi 404

@app.route('/notes', methods=['POST'])  # Route để thêm mới ghi chú (POST)
def add_note():
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
    data['id'] = max([n['id'] for n in db['notes']] or [0]) + 1  # Tạo ID mới cho ghi chú
    db['notes'].append(data)  # Thêm ghi chú mới vào danh sách
    save_db()  # Lưu lại dữ liệu vào file db.json
    return jsonify(data), 201  # Trả về ghi chú mới và mã trạng thái 201 (Created)

@app.route('/notes/<int:note_id>', methods=['PUT'])  # Route để cập nhật ghi chú theo ID (PUT)
def update_note(note_id):
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
    for i, note in enumerate(db['notes']):  # Duyệt qua tất cả ghi chú trong db
        if note['id'] == note_id:  # Nếu tìm thấy ghi chú có ID trùng khớp
            data['id'] = note_id  # Gán lại ID cho ghi chú
            db['notes'][i] = data  # Cập nhật ghi chú trong db
            save_db()  # Lưu lại dữ liệu vào file db.json
            return jsonify(data)  # Trả về ghi chú đã được cập nhật
    return jsonify({'error': 'Note not found'}), 404  # Nếu không tìm thấy ghi chú, trả về lỗi 404

@app.route('/notes/<int:note_id>', methods=['DELETE'])  # Route để xóa ghi chú theo ID (DELETE)
def delete_note(note_id):
    for i, note in enumerate(db['notes']):  # Duyệt qua tất cả ghi chú trong db
        if note['id'] == note_id:  # Nếu tìm thấy ghi chú có ID trùng khớp
            del db['notes'][i]  # Xóa ghi chú khỏi danh sách
            save_db()  # Lưu lại dữ liệu vào file db.json
            return jsonify({'message': 'Note deleted'})  # Trả về thông báo xóa thành công
    return jsonify({'error': 'Note not found'}), 404  # Nếu không tìm thấy ghi chú, trả về lỗi 404

# ──────────────── Accounts ────────────────

@app.route('/accounts', methods=['GET'])  # Route để lấy tất cả tài khoản (GET)
def get_accounts():
    for account in db['accounts']:  # Duyệt qua tất cả các tài khoản
        account.setdefault('status', 'active')  # Nếu không có 'status', gán mặc định là 'active'
    return jsonify(db['accounts'])  # Trả về tất cả tài khoản dưới dạng JSON

@app.route('/accounts/<int:account_id>', methods=['GET'])  # Route để lấy tài khoản theo ID (GET)
def get_account_by_id(account_id):
    account = next((a for a in db['accounts'] if a.get('id') == account_id), None)  # Tìm tài khoản theo ID
    if account:
        return jsonify(account)  # Trả về tài khoản nếu tìm thấy
    return jsonify({'error': 'Account not found'}), 404  # Trả về lỗi nếu không tìm thấy tài khoản

@app.route('/accounts', methods=['POST'])  # Route để tạo tài khoản mới (POST)
def create_account():
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
    data['id'] = max([a['id'] for a in db['accounts']] or [0]) + 1  # Tạo ID mới cho tài khoản
    data.setdefault('status', 'active')  # Nếu không có status, gán mặc định là 'active'
    db['accounts'].append(data)  # Thêm tài khoản mới vào danh sách
    save_db()  # Lưu lại dữ liệu vào file db.json
    return jsonify(data), 201  # Trả về tài khoản mới và mã trạng thái 201 (Created)

@app.route('/accounts/<int:account_id>', methods=['PATCH'])  # Route để cập nhật tài khoản theo ID (PATCH)
def patch_account(account_id):
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
    account = next((a for a in db['accounts'] if a['id'] == account_id), None)  # Tìm tài khoản theo ID
    if not account:
        return jsonify({'error': 'Account not found'}), 404  # Nếu không tìm thấy tài khoản, trả về lỗi 404

    account.update(data)  # Cập nhật tài khoản với dữ liệu mới
    save_db()  # Lưu lại dữ liệu vào file db.json
    return jsonify(account)  # Trả về tài khoản đã được cập nhật

@app.route('/accounts/<int:account_id>', methods=['PUT'])  # Route để thay thế tài khoản theo ID (PUT)
def update_account(account_id):
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
    for i, acc in enumerate(db['accounts']):  # Duyệt qua tất cả tài khoản trong db
        if acc['id'] == account_id:  # Nếu tìm thấy tài khoản có ID trùng khớp
            data['id'] = account_id  # Gán lại ID cho tài khoản
            db['accounts'][i] = data  # Cập nhật tài khoản trong db
            save_db()  # Lưu lại dữ liệu vào file db.json
            return jsonify(data)  # Trả về tài khoản đã được thay thế
    return jsonify({'error': 'Account not found'}), 404  # Nếu không tìm thấy tài khoản, trả về lỗi 404

@app.route('/accounts/<int:account_id>', methods=['DELETE'])  # Route để xóa tài khoản theo ID (DELETE)
def delete_account(account_id):
    for i, acc in enumerate(db['accounts']):  # Duyệt qua tất cả tài khoản trong db
        if acc['id'] == account_id:  # Nếu tìm thấy tài khoản có ID trùng khớp
            del db['accounts'][i]  # Xóa tài khoản khỏi danh sách
            save_db()  # Lưu lại dữ liệu vào file db.json
            return jsonify({'message': 'Account deleted'})  # Trả về thông báo xóa thành công
    return jsonify({'error': 'Account not found'}), 404  # Nếu không tìm thấy tài khoản, trả về lỗi 404

@app.route('/login', methods=['POST'])  # Route để đăng nhập (POST)
def login():
    data = request.get_json()  # Lấy dữ liệu JSON từ yêu cầu
    username = data.get('username')  # Lấy tên người dùng từ dữ liệu
    password = data.get('password')  # Lấy mật khẩu từ dữ liệu
    user = next(
        (u for u in db['accounts']
         if u.get('username') == username and
            u.get('password') == password and
            u.get('status', 'active') == 'active'),
        None
    )  # Tìm tài khoản với username và password khớp, và trạng thái 'active'
    if user:
        return jsonify({'message': 'Login successful', 'id': user.get('id'), 'username': user['username']})
    return jsonify({'error': 'Invalid credentials'}), 401  # Nếu không tìm thấy tài khoản, trả về lỗi 401

# ──────────────── Run ────────────────

if __name__ == '__main__':  # Chạy ứng dụng Flask
    app.run(host='0.0.0.0', port=10000, debug=True)  # Khởi chạy server ở cổng 10000, debug=True cho phép dễ dàng debug
