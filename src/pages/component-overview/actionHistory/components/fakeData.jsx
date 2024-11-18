// fakeData.js

const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };
  
  const devices = [
    { type: 'Đèn', count: 10 },
    { type: 'Quạt', count: 10 },
    { type: 'Điều Hòa', count: 10 }
  ];
  const actions = ['Bật', 'Tắt'];
  
  const generateRandomAction = () => actions[Math.floor(Math.random() * actions.length)];
  
  const generateRandomDate = (daysBack) => {
    const date = new Date();
    date.setDate(date.getDate() - Math.floor(Math.random() * daysBack));
    return date;
  };
  
  const generateFakeData = () => {
    const data = [];
    let idCounter = 1;
  
    devices.forEach(device => {
      for (let i = 0; i < device.count; i++) {
        const randomDate = generateRandomDate(10); // Random trong khoảng 10 ngày gần đây
        const formattedDate = formatDate(randomDate);
  
        data.push({
          key: idCounter,
          id: `TB${idCounter}`,  // ID thiết bị
          deviceName: `${device.type} ${idCounter}`, // Tên thiết bị
          action: generateRandomAction(), // Hành động ngẫu nhiên
          time: formattedDate, // Thời gian ngẫu nhiên
        });
  
        idCounter++;
      }
    });
  
    return data;
  };
  
  const fakeData = generateFakeData();
  
  export default fakeData;
  