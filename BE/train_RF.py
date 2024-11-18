import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import joblib

data=pd.read_csv("E:/3.hocki1nam4\IoT\BTL_IOT_FE\BE\data\smoke_detection_iot.csv")
scaler = MinMaxScaler()
X = data[["Temperature[C]", "Humidity[%]", "TVOC[ppb]", "eCO2[ppm]", "Raw Ethanol"]]
y = data["Fire Alarm"]
# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Khởi tạo mô hình Random Forest với các tham số tối ưu
model = RandomForestClassifier(
    n_estimators=200,
    max_features='sqrt',
    max_depth=None,
    criterion='log_loss',
    random_state=42
)

# Huấn luyện mô hình
model.fit(X_train, y_train)
joblib.dump(model, 'E:/3.hocki1nam4\IoT\BTL_IOT_FE\BE\weight/random_forest_model.joblib')
# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá độ chính xác của mô hình
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

