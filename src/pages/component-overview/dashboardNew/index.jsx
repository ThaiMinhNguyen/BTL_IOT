import React, { useState, useEffect } from 'react';
import { Col, Row, Card, Switch, message } from 'antd';
import ControlPanel from './components/ControlPanel'; // Import component ControlPanel
import Chart from './components/Chart';
import GasChart from './components/GasChart'; // Import GasChart
import Chatbot from './components/Chatbot';
import InfoCards from './components/InfoCards';
import "./dashboardNew.scss";

export default function DashboardNew() {
  const [data, setData] = useState([]);
  const [gasData, setGasData] = useState([]);
  const [aqi, setAqi] = useState(50);
  const [advice, setAdvice] = useState("Không khí ở mức tốt. Bạn có thể thoải mái hoạt động ngoài trời."); // Lời khuyên ban đầu
  const [isAutoMode, setIsAutoMode] = useState(true); // Chế độ tự động

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch('http://localhost:5000/api/sensor_data');
  //       const result = await response.json();
  //       setData(result.slice(-60));
  //     } catch (error) {
  //       message.error('Lỗi khi lấy dữ liệu từ API');
  //       console.error('Error fetching data:', error);
  //     }
  //   };

  //   fetchData();

  //   const intervalId = setInterval(() => {
  //     fetchData();
  //   }, 5000);

  //   return () => clearInterval(intervalId);
  // }, []);

  useEffect(() => {
    const generateFakeData = () => {
      // Dữ liệu giả cho cảm biến môi trường
      const fakeEnvData = Array.from({ length: 60 }, (_, i) => ({
        time: new Date().toLocaleTimeString(),
        temperature: Math.floor(Math.random() * 10) + 20, // Nhiệt độ từ 20-30
        humidity: Math.floor(Math.random() * 50) + 50, // Độ ẩm từ 50-100
        light: Math.floor(Math.random() * 1000) + 200, // Ánh sáng từ 200-1200
      }));
      setData(fakeEnvData);

      // Dữ liệu giả cho các chất khí
      const fakeGasData = Array.from({ length: 60 }, (_, i) => ({
        time: new Date().toLocaleTimeString(),
        NH3: Math.floor(Math.random() * 100) + 20, // NH3 từ 20-120
        NOx: Math.floor(Math.random() * 50) + 10, // NOx từ 10-60
        C6H6: Math.floor(Math.random() * 80) + 20, // C6H6 từ 20-100
        C2H5OH: Math.floor(Math.random() * 100) + 30, // C2H5OH từ 30-130
        CO2: Math.floor(Math.random() * 30) + 10, // CO2 từ 10-40
      }));
      setGasData(fakeGasData);
    };

    generateFakeData();

    const randomAqi = Math.floor(Math.random() * 150) + 1; // AQI từ 1-150
    setAqi(randomAqi);
    if (randomAqi <= 50) {
      setAdvice("Không khí ở mức tốt. Bạn có thể thoải mái hoạt động ngoài trời.");
    } else if (randomAqi <= 100) {
      setAdvice("Không khí ở mức trung bình. Người nhạy cảm nên hạn chế hoạt động ngoài trời.");
    } else {
      setAdvice("Không khí ở mức kém. Hạn chế ra ngoài, đặc biệt là nhóm nhạy cảm.");
    }

    const intervalId = setInterval(() => {
      generateFakeData();
    }, 5000);

    return () => clearInterval(intervalId);
  }, []);

  const latestData = data[data.length - 1] || { temperature: 0, humidity: 0 };

  return (
    <div className="dashboardNew">
      <InfoCards
        temperature={latestData.temperature}
        humidity={latestData.humidity}
        light={latestData.light}
      /> {/* Truyền dữ liệu vào InfoCards */}

      {/* Component Chatbot */}
      <Chatbot aqi={aqi} advice={advice} />

      {/* Khối điều khiển thiết bị và hiển thị chất */}
      <Row gutter={20} className="control-and-quality">
        <Col span={16}>
          <ControlPanel /> {/* Sử dụng component ControlPanel */}
        </Col>
        <Col span={8}>
          <Card className="quality-list">
            <h3>Các chất</h3>
            <ul>
              <li>NH₃: 50</li>
              <li>NOx: 30</li>
              <li>C₆H₆: 70</li>
              <li>C₂H₅OH: 90</li>
              <li>CO₂: 10</li>
            </ul>
          </Card>
        </Col>
      </Row>

      {/* Biểu đồ */}
      <Row className="chart-section" gutter={[16, 16]}>
        {/* Biểu đồ đầu tiên */}
        <Col span={12}>
          <Card className="chart-container">
            <Chart data={data} />
          </Card>
        </Col>

        {/* Biểu đồ thứ hai */}
        <Col span={12}>
          <Card className="chart-container">
            <GasChart data={gasData} />
          </Card>
        </Col>
      </Row>

    </div>
  );
}
