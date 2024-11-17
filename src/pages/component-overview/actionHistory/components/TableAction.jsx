import React from 'react';
import { Table } from 'antd';
import fakeData from './fakeData';  // Import dữ liệu giả từ file fakeData.js

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
      { text: 'Quạt', value: 'Quạt' },
      { text: 'Điều Hòa', value: 'Điều Hòa' },
    ],
    onFilter: (value, record) => record.deviceName.includes(value),
  },
  {
    title: 'Hành động',
    dataIndex: 'action',
    width: 100,
    filters: [
      { text: 'Bật', value: 'Bật' },
      { text: 'Tắt', value: 'Tắt' },
    ],
    onFilter: (value, record) => record.action.includes(value),
  },
  {
    title: 'Thời gian',
    dataIndex: 'time',
    width: 200,
    // Giả sử bạn muốn lọc theo một khoảng thời gian cụ thể
    filters: [
      { text: 'Hôm nay', value: 'today' },
      { text: 'Hôm qua', value: 'yesterday' },
      { text: 'Tuần này', value: 'this_week' },
    ],
    onFilter: (value, record) => {
      const today = new Date();
      const recordDate = new Date(record.time);
      switch (value) {
        case 'today':
          return recordDate.toDateString() === today.toDateString();
        case 'yesterday':
          const yesterday = new Date(today);
          yesterday.setDate(yesterday.getDate() - 1);
          return recordDate.toDateString() === yesterday.toDateString();
        case 'this_week':
          const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay()));
          return recordDate >= startOfWeek;
        default:
          return false;
      }
    },
  },
];

const TableAction = () => (
  <Table
    columns={columns}
    dataSource={fakeData}  // Sử dụng dữ liệu giả đã import
    pagination={{
      defaultPageSize: 10,  // Số lượng bản ghi mặc định mỗi trang
      showSizeChanger: true,  // Cho phép thay đổi số lượng bản ghi mỗi trang
      pageSizeOptions: ['5', '10', '15', '20'],  // Các tùy chọn số lượng bản ghi mỗi trang
    }}
    scroll={{
      y: 500,
    }}
  />
);

export default TableAction;
