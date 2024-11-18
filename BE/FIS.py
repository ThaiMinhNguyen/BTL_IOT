import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calculate_aqi(co2, co, no2, so2):
    co2 = max(0, min(co2, 1499))  # Giới hạn trong khoảng [0, 1000]
    co = max(0, min(co, 99))     # Giới hạn trong khoảng [0, 100]
    no2 = max(0, min(no2, 149))   # Giới hạn trong khoảng [0, 200]
    so2 = max(0, min(so2, 79))   # Giới hạn trong khoảng [0, 200]
    # Khởi tạo các biến mờ (fuzzy variables)
    co2_level = ctrl.Antecedent(np.arange(0, 1501, 1), 'CO2')
    co_level = ctrl.Antecedent(np.arange(0, 101, 1), 'CO')
    no2_level = ctrl.Antecedent(np.arange(0, 151, 1), 'NO2')
    so2_level = ctrl.Antecedent(np.arange(0, 81, 1), 'SO2')
    aqi = ctrl.Consequent(np.arange(0, 351, 1), 'AQI')

    co2_level['low'] = fuzz.trimf(co2_level.universe, [0, 350, 450])  # Mức thấp: 0-450 ppm (phổ biến trong phòng sạch)
    co2_level['medium'] = fuzz.trimf(co2_level.universe, [400, 600, 800])  # Mức trung bình: 400-800 ppm (phòng không có thông gió tốt)
    co2_level['high'] = fuzz.trimf(co2_level.universe, [750, 1000, 1500])  # Mức cao: 750-1500 ppm (có thể gây mệt mỏi)

    # Định nghĩa mức CO cho phòng
    co_level['low'] = fuzz.trimf(co_level.universe, [0, 0, 25])  # Mức thấp: 0-25 ppm (không có CO trong phòng)
    co_level['medium'] = fuzz.trimf(co_level.universe, [10, 25, 50])  # Mức trung bình: 10-50 ppm (thường gặp trong phòng có các thiết bị đốt)
    co_level['high'] = fuzz.trimf(co_level.universe, [30, 50, 100])  # Mức cao: 30-100 ppm (cần cảnh giác với mức này)


     # Định nghĩa mức NO2 cho phòng
    no2_level['low'] = fuzz.trimf(no2_level.universe, [0, 0, 25])  # Mức thấp: 0-25 ppm (không có NO2 trong phòng)
    no2_level['medium'] = fuzz.trimf(no2_level.universe, [20, 40, 60])  # Mức trung bình: 20-60 ppm (phòng có ít ô nhiễm NO2)
    no2_level['high'] = fuzz.trimf(no2_level.universe, [50, 100, 150])  # Mức cao: 50-150 ppm (mức ô nhiễm cao, cần thông gió)


     # Định nghĩa mức SO2 cho phòng
    so2_level['low'] = fuzz.trimf(so2_level.universe, [0, 0, 25])  # Mức thấp: 0-25 ppm (không có SO2 trong phòng)
    so2_level['medium'] = fuzz.trimf(so2_level.universe, [10, 20, 40])  # Mức trung bình: 10-40 ppm (mức SO2 nhẹ)
    so2_level['high'] = fuzz.trimf(so2_level.universe, [25, 50, 80])  # Mức cao: 25-80 ppm (cần thông gió tốt nếu có mức này)

    # Định nghĩa các mức AQI
    aqi['good'] = fuzz.trimf(aqi.universe, [0, 0, 50])
    aqi['moderate'] = fuzz.trimf(aqi.universe, [50, 100, 150])
    aqi['unhealthy_for_sensitive_groups'] = fuzz.trimf(aqi.universe, [100, 150, 200])
    aqi['unhealthy'] = fuzz.trimf(aqi.universe, [150, 200, 250])
    aqi['very_unhealthy'] = fuzz.trimf(aqi.universe, [200, 250, 300])
    aqi['hazardous'] = fuzz.trimf(aqi.universe, [200, 250, 350])

    # Định nghĩa các quy tắc
    rules = [
        # Quy tắc cho CO2, CO, NO2, SO2 ở các mức độ khác nhau
        # Các quy tắc cho mức CO2 thấp
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['low'] & so2_level['low'], aqi['good']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['low'] & so2_level['medium'], aqi['good']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['low'] & so2_level['high'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['medium'] & so2_level['low'], aqi['good']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['medium'] & so2_level['medium'], aqi['moderate']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['medium'] & so2_level['high'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['high'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['high'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['low'] & no2_level['high'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['low'] & so2_level['low'], aqi['good']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['low'] & so2_level['medium'], aqi['moderate']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['low'] & so2_level['high'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['medium'] & so2_level['low'], aqi['moderate']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['medium'] & so2_level['medium'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['medium'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['high'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['high'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['medium'] & no2_level['high'] & so2_level['high'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['low'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['low'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['low'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['medium'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['medium'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['medium'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['high'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['high'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['low'] & co_level['high'] & no2_level['high'] & so2_level['high'], aqi['hazardous']),

        # Các quy tắc cho mức CO2 trung bình
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['low'] & so2_level['low'], aqi['good']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['low'] & so2_level['medium'], aqi['moderate']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['low'] & so2_level['high'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['medium'] & so2_level['low'], aqi['moderate']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['medium'] & so2_level['medium'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['medium'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['high'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['high'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['low'] & no2_level['high'] & so2_level['high'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['low'] & so2_level['low'], aqi['moderate']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['low'] & so2_level['medium'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['low'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['medium'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['medium'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['medium'] & so2_level['high'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['high'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['high'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['medium'] & no2_level['high'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['low'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['low'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['low'] & so2_level['high'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['medium'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['medium'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['medium'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['high'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['high'] & so2_level['medium'], aqi['hazardous']),
        ctrl.Rule(co2_level['medium'] & co_level['high'] & no2_level['high'] & so2_level['high'], aqi['hazardous']),

        # Các quy tắc cho mức CO2 cao
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['low'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['low'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['low'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['medium'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['medium'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['medium'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['high'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['high'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['low'] & no2_level['high'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['low'] & so2_level['low'], aqi['unhealthy_for_sensitive_groups']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['low'] & so2_level['medium'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['low'] & so2_level['high'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['medium'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['medium'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['medium'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['high'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['high'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['medium'] & no2_level['high'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['low'] & so2_level['low'], aqi['unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['low'] & so2_level['medium'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['low'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['medium'] & so2_level['low'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['medium'] & so2_level['medium'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['medium'] & so2_level['high'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['high'] & so2_level['low'], aqi['very_unhealthy']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['high'] & so2_level['medium'], aqi['hazardous']),
        ctrl.Rule(co2_level['high'] & co_level['high'] & no2_level['high'] & so2_level['high'], aqi['hazardous']),

    ]

    # Tạo hệ thống điều khiển mờ
    aqi_control_system = ctrl.ControlSystem(rules)
    aqi_simulation = ctrl.ControlSystemSimulation(aqi_control_system)

    # Cung cấp đầu vào cho hệ thống
    aqi_simulation.input['CO2'] = co2
    aqi_simulation.input['CO'] = co
    aqi_simulation.input['NO2'] = no2
    aqi_simulation.input['SO2'] = so2
    
    # Tính toán đầu ra
    aqi_simulation.compute()
    print(aqi_simulation.output)
        # Kiểm tra đầu ra và trả về giá trị AQI dự đoán
    if 'AQI' in aqi_simulation.output:
        print(f"AQI: {aqi_simulation.output['AQI']}")
        return aqi_simulation.output['AQI']
    else:
        print("AQI not calculated, check rules or input values.")
        return 30

# # print(calculate_aqi(400, 20, 50, 25))
# print(calculate_aqi(78204.44, 1.14, 1.56, 1.9))