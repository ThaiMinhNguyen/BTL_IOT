const formatDate = (date) => {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
};

// Hàm này sẽ trả về thời gian hiện tại
const getCurrentDate = () => {
  return new Date();
};

// Hàm này sẽ tạo ngày giờ lùi lại 5 phút cho mỗi bản ghi
const generateFakeData = (id, offsetMinutes) => {
  const currentDate = getCurrentDate(); // Lấy thời gian hiện tại
  currentDate.setMinutes(currentDate.getMinutes() - offsetMinutes); // Giảm đi số phút
  return {
    id: id,
    temperature: (Math.random() * 10 + 20).toFixed(2), // Nhiệt độ từ 20°C đến 30°C
    light: (Math.random() * 100).toFixed(2),           // Ánh sáng từ 0 đến 100 lux
    humidity: (Math.random() * 30 + 50).toFixed(2),    // Độ ẩm từ 50% đến 80%
    time: formatDate(currentDate),                     // Thời gian với định dạng ngày-tháng-năm
  };
};

// Tạo mảng dữ liệu giả gồm 30 bản ghi, mỗi bản ghi cách nhau 5 phút
const fakeData = Array.from({ length: 30 }, (_, index) => generateFakeData(index + 1, index * 5));

export default fakeData;
