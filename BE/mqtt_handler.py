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
    # print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe("esp/dht11")
    client.subscribe("esp/bh1750")
    client.subscribe("esp/mq135")

# Cập nhật hàm khởi tạo MQTT để tránh cảnh báo về API cũ
def connect_mqtt(broker="192.168.43.35", port=1883, username="thang", password="thang1411"):
    mqtt_client = mqtt.Client()

    # Cập nhật sử dụng API mới
    mqtt_client.username_pw_set(username, password)
    
    # Đăng ký các callback bằng phương thức riêng biệt
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(broker, port, 60)
    return mqtt_client

# Hàm để bắt đầu nhận dữ liệu từ MQTT
def mqtt_loop():
    mqtt_client = connect_mqtt()  # Kết nối đến broker
    mqtt_client.loop_start()  # Bắt đầu vòng lặp nhận dữ liệu
    while dht11_data != {} or bh1750_data != {} or mq135_data != {}:
        mqtt_client.loop_stop()
    return dht11_data, bh1750_data, mq135_data


