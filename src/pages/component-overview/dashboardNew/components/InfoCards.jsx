import React from 'react';
import { Col, Row, Card } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTemperatureHigh, faSun, faTint } from '@fortawesome/free-solid-svg-icons';
import "./InfoCards.scss"

const InfoCards = ({ temperature, humidity, light }) => {
  return (
    <Row gutter={15} className='list-card'>
      <Col span={8}>
        <Card bordered={false} className='card-item temperature'>
          <div>Nhiệt độ: {temperature}°C</div> {/* Hiển thị nhiệt độ */}
          <div className='icon'>
            <FontAwesomeIcon icon={faTemperatureHigh} /> 
          </div>
        </Card>
      </Col>
      <Col span={8}>
        <Card bordered={false} className='card-item humidity'>
          <div>Độ ẩm: {humidity}%</div> {/* Hiển thị độ ẩm */}
          <div className='icon'>
            <FontAwesomeIcon icon={faTint} /> 
          </div>
        </Card>
      </Col>
      <Col span={8}>
        <Card bordered={false} className='card-item light'>
          <div>Ánh sáng: {light} lux</div> {/* Hiển thị ánh sáng */}
          <div className='icon'>
            <FontAwesomeIcon icon={faSun} /> 
          </div>
        </Card>
      </Col>
    </Row>
  );
};

export default InfoCards;
