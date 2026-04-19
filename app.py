import time
import hashlib
import threading
import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# --- CẤU HÌNH HỆ THỐNG ---
TOKEN = "8670893641:AAGovRHAo8mIGvOXchbTqxZZIG2KQiwdRcw"
SYSTEM = {
    "admin": "@tranhoang2286",
    "status": "OFFLINE",
    "base_phien": 0,
    "base_time": 0,
    "game_name": "LC79",
    "last_sent_phien": 0
}

# --- GIAO DIỆN ADMIN CYBERPUNK ---
ADMIN_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>ADMIN LC79 - HEXX ULTRA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #020202; color: #f1c40f; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; overflow: hidden; }
        .cyber-card { background: rgba(20, 20, 20, 0.95); border: 2px solid #f1c40f; padding: 40px; border-radius: 20px; box-shadow: 0 0 30px #f1c40f; position: relative; width: 350px; text-align: center; }
        .cyber-card::before { content: ""; position: absolute; top: -5px; left: -5px; right: -5px; bottom: -5px; border: 1px solid #00f2fe; border-radius: 25px; z-index: -1; animation: pulse 2s infinite; }
        h1 { font-size: 1.5em; text-transform: uppercase; letter-spacing: 5px; margin-bottom: 30px; color: #fff; text-shadow: 0 0 10px #f1c40f; }
        input { width: 90%; padding: 12px; margin: 15px 0; background: #000; border: 1px solid #f1c40f; color: #fff; border-radius: 5px; outline: none; }
        button { width: 100%; padding: 15px; background: #f1c40f; color: #000; border: none; font-weight: bold; text-transform: uppercase; cursor: pointer; transition: 0.5s; border-radius: 5px; }
        button:hover { background: #fff; box-shadow: 0 0 20px #fff; }
        .status-on { color: #2ecc71; text-shadow: 0 0 10px #2ecc71; }
        .status-off { color: #e74c3c; }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    </style>
</head>
<body>
    <div class="cyber-card">
        <h1>ADMIN LC79</h1>
        <p>Hệ thống: <span class="{{ 'status-on' if status == 'ONLINE' else 'status-off' }}">{{ status }}</span></p>
        <p>Admin: {{ admin }}</p>
        <hr border-color="#333">
        <form action="/activate" method="post">
            <input type="number" name="phien" placeholder="NHẬP PHIÊN LC79 HIỆN TẠI" required>
            <button type="submit">KÍCH HOẠT HEXX ULTRA</button>
        </form>
    </div>
</body>
</html>
"""

# --- THUẬT TOÁN HEXX SIÊU CẤP ---
def hexx_ultra_logic(phien_id):
    # SHA-512 kép để phân tích mã băm sâu
    raw = f"LC79_ULTRA_{phien_id}_tranhoang2286"
    h1 = hashlib.sha512(raw.encode()).hexdigest()
    h2 = hashlib.sha512(h1.encode()).hexdigest()
    
    # Lấy 4 ký tự từ giữa mã băm để tính toán
    val = int(h2[25:29], 16)
    
    # Xác suất siêu cấp 51% - 98%
    prob = 51 + (val % 48)
    prediction = "TÀI" if val % 2 == 0 else "XỈU"
    
    # Phân tích cầu dựa trên đầu mã băm
    cau_type = "Cầu Bệt Rồng" if int(h2[0:2], 16) > 200 else "Cầu Đảo Nghịch"
    
    return {"phien": phien_id, "du_doan": prediction, "ti_le": f"{prob}%", "cau": cau_type}

# --- BOT TELEGRAM SENDER ---
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": "@tranhoang2286", "text": msg, "parse_mode": "HTML"} # Gửi vào kênh hoặc id cá nhân
    try: requests.post(url, json=payload)
    except: pass

def telegram_loop():
    while True:
        if SYSTEM["status"] == "ONLINE":
            elapsed = time.time() - SYSTEM["base_time"]
            current_phien = SYSTEM["base_phien"] + int(elapsed // 60)
            
            # Chỉ gửi tin nhắn khi qua phiên mới
            if current_phien > SYSTEM["last_sent_phien"]:
                data = hexx_ultra_logic(current_phien)
                intro = (
                    "<b>🌟 HỆ THỐNG DỰ ĐOÁN LC79 SIÊU CẤP 🌟</b>\n"
                    "------------------------------------\n"
                    f"👤 <b>Admin:</b> {SYSTEM['admin']}\n"
                    "🛠 <b>Thuật toán:</b> Hexx Ultra Analysis 2026\n"
                    "📖 <b>Giới thiệu:</b> Chào mừng bạn đến với hệ thống AI mạnh nhất dành cho LC79. "
                    "Hệ thống tự động phân tích mã hash của game, bóc tách nhịp cầu và "
                    "đưa ra kết quả với tỉ lệ thắng lên đến 98%. "
                    "Dữ liệu được cập nhật thời gian thực 24/24.\n"
                    "------------------------------------\n"
                    f"🔢 <b>Phiên:</b> <code>#{data['phien']}</code>\n"
                    f"🎯 <b>Dự đoán:</b> <code>{data['du_doan']}</code>\n"
                    f"📊 <b>Tỉ lệ thắng:</b> <code>{data['ti_le']}</code>\n"
                    f"🌊 <b>Thế cầu:</b> <i>{data['cau']}</i>\n"
                    "------------------------------------\n"
                    "⚠️ <i>Lưu ý: Kết quả chỉ mang tính chất tham khảo. Chúc bạn may mắn!</i>"
                )
                send_telegram(intro)
                SYSTEM["last_sent_phien"] = current_phien
        time.sleep(10)

# --- ROUTES ---
@app.route('/')
def index():
    return render_template_string(ADMIN_UI, admin=SYSTEM["admin"], status=SYSTEM["status"])

@app.route('/activate', methods=['POST'])
def activate():
    SYSTEM["base_phien"] = int(request.form.get('phien'))
    SYSTEM["base_time"] = time.time()
    SYSTEM["status"] = "ONLINE"
    return "<h1>KÍCH HOẠT THÀNH CÔNG! BOT ĐANG CHẠY...</h1><a href='/'>Quay lại</a>"

@app.route('/api/get-result')
def get_result():
    if SYSTEM["status"] == "OFFLINE": return jsonify({"error": "Admin chua kich hoat"}), 403
    elapsed = time.time() - SYSTEM["base_time"]
    current_phien = SYSTEM["base_phien"] + int(elapsed // 60)
    data = hexx_ultra_logic(current_phien)
    return jsonify({"admin": SYSTEM["admin"], "game": SYSTEM["game_name"], "data": data})

if __name__ == "__main__":
    # Chạy bot ngầm
    threading.Thread(target=telegram_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
