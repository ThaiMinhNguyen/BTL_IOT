import threading
import paho.mqtt.client as mqtt
import json
import time

# Biến lưu trữ dữ liệu nhận từ MQTT theo từng topic
dht11_data = {}
bh1750_data = {}
mq135_data = {}

# Hàm callback khi nhận được thông điệp từ MQTT
def on_message(client, userdata, msg):
    global dht11_data, bh1750_data, mq135_data
    try:
        # Chuyển đổi payload thành dict (dữ liệu gửi dưới dạng JSON)
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        data = msg.payload.decode()

    # Cập nhật dữ liệu theo topic
    if msg.topic == "esp/dht11":
        dht11_data = data
    elif msg.topic == "esp/bh1750":
        bh1750_data = data
    elif msg.topic == "esp/mq135":
        mq135_data = data

# Hàm callback khi kết nối tới MQTT Broker thành công
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe("esp/dht11")
    client.subscribe("esp/bh1750")
    client.subscribe("esp/mq135")

# Hàm khởi tạo MQTT
def connect_mqtt(broker="192.168.43.35", port=1883, username="thang", password="thang1411"):
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username, password)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(broker, port, 60)
    return mqtt_client

# Hàm chạy vòng lặp MQTT
def mqtt_loop():
    mqtt_client = connect_mqtt()
    mqtt_client.loop_forever()  # Duy trì vòng lặp nhận dữ liệu từ broker

# Chạy MQTT loop ẩn trong background bằng Thread
def start_mqtt_in_background():
    mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()
    print("MQTT loop started in the background")
def get_data():
    return dht11_data, bh1750_data, mq135_data
# Chương trình chính
if __name__ == "__main__":
    # Khởi động MQTT loop trong background
    start_mqtt_in_background()

    # Chương trình chính vẫn tiếp tục chạy
    while True:
        print("DHT11 Data:", dht11_data)
        print("BH1750 Data:", bh1750_data)
        print("MQ135 Data:", mq135_data)
        print("Main program is running...")
        time.sleep(5)
