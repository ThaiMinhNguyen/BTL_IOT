import React, { useState, useEffect } from 'react';
import { Card, Switch, InputNumber, Button } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFan, faLightbulb, faDoorClosed, faDoorOpen } from '@fortawesome/free-solid-svg-icons';
import './ControlPanel.scss';

const ControlPanel = ({ onChange }) => {
  const [isAutoMode, setIsAutoMode] = useState(true); // Chế độ tự động
  const [fanOn, setFanOn] = useState(false);
  const [lights, setLights] = useState([false]);
  const [doorClosed, setDoorClosed] = useState(false);
  const [lightTime, setLightTime] = useState(0);
  const [countdown, setCountdown] = useState(0); // Thời gian đếm ngược
  const [isCounting, setIsCounting] = useState(false); // Kiểm tra xem đồng hồ đếm ngược đang chạy hay không

  const sendDataToServer = async (data) => {
    try {
      const response = await fetch("http://localhost:5000/api/control", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        console.log("Data saved successfully");
      } else {
        console.error("Failed to save data");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  

  const handleModeChange = (checked) => {
    setIsAutoMode(checked);
    if (!checked) {
      // Reset thời gian đếm ngược khi chuyển sang chế độ thủ công
      setCountdown(0);
      setIsCounting(false);
    }
    onChange?.(checked);
    const state = checked ? "on" : "off";  // Chuyển đổi thành "on" hoặc "off"
    sendDataToServer({ type: "mode", state: state });
  };

  const handleFanChange = (checked) => {
    setFanOn(checked);
    onChange?.(checked);
    const state = checked ? "on" : "off";  // Chuyển đổi thành "on" hoặc "off"
    sendDataToServer({ type: "fan", state: state });
  };

  const handleLightChange = (index, checked) => {
    const newLights = [...lights];
    newLights[index] = checked;
    setLights(newLights);
    onChange?.(checked);
    const state = checked ? "on" : "off";  // Chuyển đổi thành "on" hoặc "off"
    sendDataToServer({ type: "light", state: state });
  };

  const handleDoorChange = (checked) => {
    setDoorClosed(!checked);
    onChange?.(!checked);
    const state = checked ? "mở" : "đóng";  
    sendDataToServer({ type: "door", state: state });
  };

  const handleSetTime = () => {
    if (lightTime > 0) {
      setCountdown(lightTime * 60); // Chuyển phút thành giây
      setIsCounting(true);
      const durationInSeconds = lightTime * 60;
      sendDataToServer({
        type: "light_timer",
        duration: durationInSeconds, // Gửi thời gian dưới dạng giây
      });
    }
  };

  useEffect(() => {
    let timer;
    if (isCounting && countdown > 0) {
      timer = setInterval(() => {
        setCountdown((prev) => prev - 1);
      }, 1000);
    } else if (countdown === 0 && isCounting) {
      setIsCounting(false);
      // Reset đèn sau khi hết thời gian
      setLights([false]); // Tắt tất cả đèn (hoặc xử lý theo yêu cầu)
    }

    return () => clearInterval(timer);
  }, [countdown, isCounting]);

  return (
    <div className="control-panel">
      <Card bordered={false} className="card-button mode-switch">
        <div>Chế độ tự động</div>
        <Switch checked={isAutoMode} onChange={handleModeChange} className="switch" />
      </Card>

      {isAutoMode ? (
        // Chế độ tự động: nhập thời gian đèn sáng
        <Card bordered={false} className="card-button auto-mode">
          <div className="time-setting">
            <FontAwesomeIcon icon={faLightbulb} className="icon light-lit" />
            Thời gian đèn sáng (phút):
            <InputNumber
              min={1}
              value={lightTime}
              onChange={(value) => setLightTime(value)}
              className="input-number"
            />
            <Button
              type="primary"
              onClick={() => {
                if (lightTime > 0) {
                  sendDataToServer({
                    type: "light_timer",
                    duration: lightTime * 60, // Gửi thời gian dưới dạng giây
                  });
                }
              }}
              disabled={isCounting && lightTime * 60 === countdown} // Disable nếu thời gian không thay đổi
            >
              Set
            </Button>
          </div>

          
        </Card>
      ) : (
        // Chế độ thủ công: bật/tắt thiết bị
        <div className="manual-mode">
          <Card bordered={false} className="card-button">
            <div>
              <FontAwesomeIcon icon={faFan} className={`icon ${fanOn ? 'spinning fan-lit' : ''}`} />
              Quạt
            </div>
            <Switch checked={fanOn} onChange={handleFanChange} className="switch" />
          </Card>

          {lights.map((lightOn, index) => (
            <Card bordered={false} className="card-button" key={index}>
              <div>
                <FontAwesomeIcon icon={faLightbulb} className={`icon ${lightOn ? 'light-lit' : ''}`} />
                Đèn {index + 1}
              </div>
              <Switch
                checked={lightOn}
                onChange={(checked) => handleLightChange(index, checked)}
                className="switch"
              />
            </Card>
          ))}

          <Card bordered={false} className="card-button">
            <div>
              <FontAwesomeIcon
                icon={doorClosed ? faDoorClosed : faDoorOpen}
                className={`icon ${doorClosed ? 'door-closed' : 'door-open'}`}
              />
              {doorClosed ? 'Đóng cửa' : 'Mở cửa'}
            </div>
            <Switch checked={!doorClosed} onChange={handleDoorChange} className="switch" />
          </Card>
        </div>
      )}
    </div>
  );
};

export default ControlPanel;