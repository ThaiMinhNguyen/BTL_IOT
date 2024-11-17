import React from 'react';
import { Row, Col, Card } from 'antd';
import './chatbot.scss';

export default function Chatbot({ aqi, advice }) {
  return (
    <div className="chatbot">
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="aqi-card" title="Chỉ số AQI">
            <h2>{aqi}</h2>
          </Card>
        </Col>
        <Col span={16}>
          <Card className="advice-card" title="Lời khuyên từ Chatbot">
            <p>{advice}</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
