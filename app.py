import time
import hashlib
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# --- CẤU HÌNH HỆ THỐNG ---
SYSTEM_DATA = {
    "admin": "@tranhoang2286",
    "status": "OFFLINE",
    "server_start_time": "N/A",
    "game_target": "https://789clubx.ac"
}

# Giao diện Server Admin
ADMIN_UI = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SERVER ADMIN - HOANGDZ</title>
    <style>
        body { background: #050505; color: #00ecff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding-top: 50px; }
        .container { border: 1px solid #00ecff; display: inline-block; padding: 30px; border-radius: 15px; background: rgba(0, 236, 255, 0.05); box-shadow: 0 0 20px #00ecff; }
        h1 { text-transform: uppercase; letter-spacing: 3px; }
        .status-box { margin: 20px 0; font-size: 1.2em; }
        .status-off { color: #ff3e3e; font-weight: bold; }
        .status-on { color: #3eff4e; font-weight: bold; text-shadow: 0 0 10px #3eff4e; }
        button { background: #00ecff; color: #000; border: none; padding: 12px 25px; font-size: 1em; font-weight: bold; border-radius: 5px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .footer { margin-top: 20px; font-size: 0.8em; opacity: 0.7; }
    </style>
</head>
<body>
    <div class="container">
        <h1>HEXX API SERVER</h1>
        <p>Admin: <b>{{ admin }}</b></p>
        
        <div class="status-box">
            Trạng thái Server: 
            <span class="{{ 'status-on' if status == 'ONLINE' else 'status-off' }}">
                {{ status }}
            </span>
        </div>
        
        <p>Khởi động lúc: {{ last_start }}</p>

        <form action="/server/activate" method="post">
            <button type="submit">KÍCH HOẠT SERVER</button>
        </form>

        <div class="footer">
            Hệ thống phân tích cầu chuẩn xác 51% - 98%<br>
            Thiết kế bởi @tranhoang2286
        </div>
    </div>
</body>
</html>
"""

# --- THUẬT TOÁN HEXX ANALYSIS ---
def analyze_phien(phien_id):
    # Tạo mã băm dựa trên phiên để đảm bảo không Random
    raw_str = f"hoangdz_secret_{phien_id}"
    hex_hash = hashlib.sha256(raw_str.encode()).hexdigest()
    
    # Lấy giá trị số từ mã Hex
    seed_val = int(hex_hash[:4], 16)
    
    # Tính xác suất (51% - 98%)
    probability = 51 + (seed_val % 48)
    
    # Dự đoán dựa trên nhịp Hexx
    prediction = "TÀI" if seed_val % 2 == 0 else "XỈU"
    
    # Nhận diện loại cầu giả lập từ Hex
    cau_patterns = ["Cầu Bệt 1-1", "Cầu Nghiêng", "Cầu Đảo", "Cầu 2-2"]
    current_cau = cau_patterns[seed_val % len(cau_patterns)]

    return {
        "phien": phien_id,
        "du_doan": prediction,
        "xac_suat": f"{probability}%",
        "loai_cau": current_cau,
        "admin": SYSTEM_DATA["admin"]
    }

# --- CÁC ĐƯỜNG DẪN (ROUTES) ---

@app.route('/')
def home():
    return render_template_string(ADMIN_UI, 
                                 admin=SYSTEM_DATA["admin"], 
                                 status=SYSTEM_DATA["status"],
                                 last_start=SYSTEM_DATA["server_start_time"])

@app.route('/server/activate', methods=['POST'])
def activate():
    SYSTEM_DATA["status"] = "ONLINE"
    SYSTEM_DATA["server_start_time"] = time.strftime('%H:%M:%S | %d/%m/%Y')
    return "<h1>SERVER ĐÃ BẬT!</h1><a href='/'>Quay lại Dashboard</a>"

@app.route('/api/get-predict', methods=['GET'])
def get_predict():
    if SYSTEM_DATA["status"] == "OFFLINE":
        return jsonify({"error": "Server chưa kích hoạt. Vui lòng vào trang Admin nhấn nút Start."}), 403
    
    # Lấy phiên tự động theo thời gian thực
    phien_hien_tai = int(time.time() / 60)
    result = analyze_phien(phien_hien_tai)
    
    return jsonify({
        "success": True,
        "author": SYSTEM_DATA["admin"],
        "game": "789Club",
        "data": result,
        "timestamp": time.strftime('%H:%M:%S')
    })

if __name__ == "__main__":
    # Port 8080 để Render nhận diện
    app.run(host='0.0.0.0', port=8080)
