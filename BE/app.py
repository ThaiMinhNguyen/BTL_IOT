from flask import Flask, jsonify
import threading
import paho.mqtt.client as mqtt
import json
import time
from FIS import calculate_aqi
from chatbot import chatbot
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from flask_cors import CORS
import os
from pymongo import MongoClient
from datetime import datetime
from flask import request
import joblib
import numpy as np
vector_index=None

app = Flask(__name__)
CORS(app)
mode_auto=False
time_auto=0
mode_fan="OFF"
mode_buzzer="OFF"
mode_door="OFF"
mode_light="OFF"
broker_address="192.168.26.113"
mqtt_client=None
control_client=None

model_RF = joblib.load('E:/3.hocki1nam4\IoT\BTL_IOT_FE\BE\weight/random_forest_model.joblib')
def predict_RF(temperature, humidity, tvoc, eco2, raw_ethanol):
# Chuyển đầu vào thành một mảng 2D vì model.predict() yêu cầu đầu vào là một mảng 2D
    input_data = np.array([[temperature, humidity, tvoc, eco2, raw_ethanol]])
    # Sử dụng mô hình để dự đoán
    prediction = model_RF.predict(input_data)
    # Trả về kết quả dự đoán
    return prediction[0]
# # # Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["home"]  # Tên database
items_collection = db["control_panel"]  # Tên collection

# API để lấy dữ liệu từ cảm biến
@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    time_out=100
    start_time=time.time()
    while dht11_data == {} or bh1750_data == {} or mq135_data == {}:
        if time.time()-start_time>time_out:
            break
        time.sleep(0.1)
    if mode_auto:
        if dht11_data['temperature']>20:
            control_topic("home/fan", "ON")
        else:
            control_topic("home/fan", "OFF")
        
        if bh1750_data['lux']<100 and time_auto>0:
            control_topic("home/light", "ON")
            time_auto-=5
        else: 
            control_topic("home/light", "OFF")
    
    fire_alarm=predict_RF(dht11_data['temperature'], dht11_data['humidity'], mq135_data['tvocppm']*1000, mq135_data['co2ppm'], mq135_data['ethanolppm'])
    if fire_alarm==1:
        control_topic("home/buzzer", "ON")
        control_topic("home/door", "ON")
        control_topic("home/fan", "ON")
    else:
        control_topic("home/buzzer", "OFF")
        control_topic("home/door", mode_door)
        control_topic("home/fan", "OFF")
    print(json.dumps({
        "dht11": dht11_data,
        "bh1750": bh1750_data,
        "mq135": mq135_data
    }))
    return jsonify({
        "dht11": dht11_data,
        "bh1750": bh1750_data,
        "mq135": mq135_data
    }), 200

@app.route('/api/aqi_chatbot', methods=['GET'])
def get_aqi_chatbot():
    aqi=calculate_aqi(mq135_data['co2ppm'], mq135_data['coppm'], mq135_data['no2ppm'], mq135_data['so2ppm'])
    if aqi>=200:
        control_topic("home/buzzer", "ON")
        control_topic("home/door", "ON")
        control_topic("home/fan", "ON")
    elif aqi >=100:
        control_topic("home/fan", "ON")
    else: 
        control_topic("home/fan", mode_fan)
        control_topic("home/buzzer", mode_buzzer)
        control_topic("home/door", mode_door)
    chatbot_response = chatbot("Chỉ số AQI là "+ str(aqi) , vector_index)
    print(chatbot_response)
    return jsonify({
        "aqi": aqi, 
        "chatbot_response": chatbot_response
    }), 200
@app.route("/api/control", methods=["POST"])
def save_control_data():
    global mode_fan, mode_door, mode_light, mode_auto
    try:
        # Lấy dữ liệu JSON từ request
        data = request.get_json()
        print(data)
        data['timestamp'] = datetime.utcnow()
        if data['type']=="fan" and data['state']=="on":
            mode_fan="ON"
            control_topic("home/fan", "ON")
        elif data['type']=="fan" and data['state']=="off":
            mode_fan="OFF"
            control_topic("home/fan", "OFF")
        elif data['type']=="door" and data['state']=="mở":
            mode_door="ON"
            control_topic("home/door", "ON")
        elif data['type']=="door" and data['state']=="đóng":
            mode_door="OFF"
            control_topic("home/door", "OFF")
        elif data['type']=="light" and data['state']=="on":
            mode_light="ON"
            control_topic("home/light", "ON")
        elif data['type']=="light" and data['state']=="off":
            mode_light="OFF"
            control_topic("home/light", "OFF")
        elif data['type']=="mode" and data['state']=="on":
            mode_auto=True
            control_topic("home/fan", "OFF")
            control_topic("home/door", "OFF")
            control_topic("home/light", "OFF")
        elif data['type']=="mode" and data['state']=="off":
            mode_auto=False
            control_topic("home/fan", mode_fan)
            control_topic("home/door", mode_door)
            control_topic("home/light", mode_light)
        # Lưu vào MongoDB
        items_collection.insert_one(data)
        
        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API để lấy dữ liệu lịch sử
@app.route('/api/history', methods=['GET'])
def get_history():
    # Tùy chọn query theo tham số
    limit = int(request.args.get('limit', 100))  # Số lượng bản ghi (default: 10)
    records = list(items_collection.find().sort("timestamp", -1).limit(limit))  # Lấy dữ liệu mới nhất
    for record in records:
        record["_id"] = str(record["_id"])  # Convert ObjectId to string
    print(jsonify(records))
    return jsonify(records), 200

def read_data(folder_path): 
    content = ""  # Biến lưu trữ nội dung gộp của các tệp
    # Duyệt qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        # Kiểm tra nếu tệp là tệp .txt
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            # Đọc nội dung của tệp và nối vào biến merged_content
            with open(file_path, 'r') as infile:
                content += infile.read() + "\n"  # Thêm dòng mới giữa các tệp
    os.environ["GOOGLE_API_KEY"] ="AIzaSyBceMs3VwqaznOPok49DaQA8m8GJiMTf4c"
    # warnings.filterwarnings("ignore")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    texts = text_splitter.split_text(content)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":1})
    return vector_index


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
def connect_mqtt(broker=broker_address, port=1883, username="thang", password="thang1411"):
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(username, password)
    mqtt_client.connect(broker, port, 60)
    return mqtt_client

# # Hàm chạy vòng lặp MQTT
def mqtt_loop():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()  # Duy trì vòng lặp nhận dữ liệu từ broker
    time.sleep(5)

# Chạy MQTT loop ẩn trong background bằng Thread
def start_mqtt_in_background():
    mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()
    print("MQTT loop started in the background")
def control_topic(topic,data):
    # Gửi thông điệp tới topic "home/fan"
    control_client.publish(topic, data)  # Thay "on" bằng dữ liệu bạn muốn gửi

if __name__ == '__main__':
    mqtt_client=connect_mqtt()
    control_client= connect_mqtt()
    start_mqtt_in_background()
    vector_index=read_data("E:/3.hocki1nam4\IoT\BTL_IOT\BE\AQI")
    app.run(host='0.0.0.0', port=5000, debug=True)
