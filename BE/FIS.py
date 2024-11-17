import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calculate_aqi(co2, co, no2, so2):
    # Khởi tạo các biến mờ (fuzzy variables)
    co2_level = ctrl.Antecedent(np.arange(0, 1001, 1), 'CO2')
    co_level = ctrl.Antecedent(np.arange(0, 101, 1), 'CO')
    no2_level = ctrl.Antecedent(np.arange(0, 201, 1), 'NO2')
    so2_level = ctrl.Antecedent(np.arange(0, 201, 1), 'SO2')
    aqi = ctrl.Consequent(np.arange(0, 501, 1), 'AQI')

    # Định nghĩa các mức độ khí CO2, CO, NO2, SO2 với 3 mức độ
    co2_level['low'] = fuzz.trimf(co2_level.universe, [0, 0, 300])
    co2_level['medium'] = fuzz.trimf(co2_level.universe, [150, 300, 600])
    co2_level['high'] = fuzz.trimf(co2_level.universe, [300, 600, 1000])

    co_level['low'] = fuzz.trimf(co_level.universe, [0, 0, 20])
    co_level['medium'] = fuzz.trimf(co_level.universe, [10, 20, 50])
    co_level['high'] = fuzz.trimf(co_level.universe, [20, 50, 100])

    no2_level['low'] = fuzz.trimf(no2_level.universe, [0, 0, 50])
    no2_level['medium'] = fuzz.trimf(no2_level.universe, [25, 50, 100])
    no2_level['high'] = fuzz.trimf(no2_level.universe, [50, 100, 200])

    so2_level['low'] = fuzz.trimf(so2_level.universe, [0, 0, 25])
    so2_level['medium'] = fuzz.trimf(so2_level.universe, [10, 25, 50])
    so2_level['high'] = fuzz.trimf(so2_level.universe, [25, 50, 100])

    # Định nghĩa các mức AQI
    aqi['good'] = fuzz.trimf(aqi.universe, [0, 0, 50])
    aqi['moderate'] = fuzz.trimf(aqi.universe, [50, 100, 150])
    aqi['unhealthy_for_sensitive_groups'] = fuzz.trimf(aqi.universe, [150, 200, 250])
    aqi['unhealthy'] = fuzz.trimf(aqi.universe, [250, 300, 350])
    aqi['very_unhealthy'] = fuzz.trimf(aqi.universe, [350, 400, 450])
    aqi['hazardous'] = fuzz.trimf(aqi.universe, [450, 500, 500])

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
    aqi_ctrl = ctrl.ControlSystem(rules)
    aqi_sim = ctrl.ControlSystemSimulation(aqi_ctrl)

    # Cung cấp các giá trị đầu vào
    aqi_sim.input['CO2'] = co2
    aqi_sim.input['CO'] = co
    aqi_sim.input['NO2'] = no2
    aqi_sim.input['SO2'] = so2

    # Tính toán AQI
    try:
        aqi_sim.compute()
    except Exception as e:
        print("Error during compute:", e)
        return None

    # Kiểm tra đầu ra và trả về giá trị AQI dự đoán
    if 'AQI' in aqi_sim.output:
        print(f"AQI: {aqi_sim.output['AQI']}")
        return aqi_sim.output['AQI']
    else:
        print("AQI not calculated, check rules or input values.")
        return None

# aqi = calculate_aqi(50, 90, 40, 20)
# print(f"Giá trị AQI dự đoán: {aqi}")
