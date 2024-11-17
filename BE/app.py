from flask import Flask, jsonify
from mqtt_handler import mqtt_loop
import time

app = Flask(__name__)
# Hàm đảm bảo dữ liệu được cập nhật trước khi trả lời
def get_data(timeout=100):
    dht11_data, bh1750_data, mq135_data = mqtt_loop()
    start_time = time.time()
    while dht11_data == {} or bh1750_data == {} or mq135_data == {}:
        dht11_data, bh1750_data, mq135_data = mqtt_loop()
        print(dht11_data, bh1750_data, mq135_data)
        if time.time() - start_time > timeout:
            break
        time.sleep(0.1)
    return dht11_data, bh1750_data, mq135_data

# API để lấy dữ liệu từ cảm biến
@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    dht11_data, bh1750_data, mq135_data=get_data()  # Đợi dữ liệu từ MQTT nếu cần
    return jsonify({
        "dht11": dht11_data,
        "bh1750": bh1750_data,
        "mq135": mq135_data
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
