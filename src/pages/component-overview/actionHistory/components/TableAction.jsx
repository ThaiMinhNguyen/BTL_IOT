import React, { useEffect, useState } from 'react';
import { Table } from 'antd';

const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    width: 150,
  },
  {
    title: 'Tên thiết bị',
    dataIndex: 'deviceName',
    width: 200,
    filters: [
      { text: 'Đèn', value: 'Đèn' },
      { text: 'Chế độ', value: 'Chế độ' },
    ],
    onFilter: (value, record) => record.deviceName.includes(value),
  },
  {
    title: 'Hành động',
    dataIndex: 'action',
    width: 100,
  },
  {
    title: 'Thời gian',
    dataIndex: 'time',
    width: 200,
  },
];

const TableAction = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch dữ liệu từ API
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch('http://localhost:5000/api/history');
        const result = await response.json();
        // Map dữ liệu từ API
        const typeMap = {
          light: 'Đèn',
          door: 'Cửa',
          fan: 'Quạt',
          mode: 'Chế độ tự động',
          light_timer: 'Bộ đếm tắt đèn',
        };
        
        const mappedData = result.map((item) => ({
          id: item._id,
          deviceName: typeMap[item.type] || 'Thiết bị không xác định', // Ánh xạ type thành tên thiết bị
          action:
            item.type === 'light_timer'
              ? `Thời gian: ${item.duration / 60} phút`
              : item.state === 'on'
              ? 'Bật'
              : 'Tắt',
          time: new Date(item.timestamp).toLocaleString(), // Format thời gian
        }));
        setData(mappedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <Table
      columns={columns}
      dataSource={data}
      rowKey="id" // Đặt key duy nhất cho mỗi hàng
      loading={loading} // Hiển thị trạng thái loading
      pagination={{
        defaultPageSize: 20,
        showSizeChanger: true,
        pageSizeOptions: ['5', '10', '15', '20'],
      }}
      scroll={{
        y: 500,
      }}
    />
  );
};

export default TableAction;