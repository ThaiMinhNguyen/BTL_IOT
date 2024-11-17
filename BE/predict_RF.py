
import numpy as np
import joblib

def predict(temperature, humidity, tvoc, eco2, raw_ethanol):
    # Tải mô hình Random Forest đã lưu
    model = joblib.load('E:/3.hocki1nam4\IoT\BTL_IOT\BE\weight/random_forest_model.joblib')
    # Chuyển đầu vào thành một mảng 2D vì model.predict() yêu cầu đầu vào là một mảng 2D
    input_data = np.array([[temperature, humidity, tvoc, eco2, raw_ethanol]])
    
    # Sử dụng mô hình để dự đoán
    prediction = model.predict(input_data)
    
    # Trả về kết quả dự đoán
    return prediction[0]

