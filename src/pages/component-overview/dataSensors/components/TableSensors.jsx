import React, { useState, useEffect } from 'react';
import { Table, Input, message } from 'antd';

const { Search } = Input;

const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    sorter: (a, b) => a.id - b.id, // Sắp xếp theo ID
  },
  {
    title: 'Temperature',
    dataIndex: 'temperature',
    sorter: (a, b) => a.temperature - b.temperature, // Sắp xếp theo Nhiệt độ
    filters: [
      { text: '20°C - 25°C', value: '20-25' },
      { text: '25°C - 30°C', value: '25-30' },
    ],
    onFilter: (value, record) => {
      const temp = parseFloat(record.temperature);
      if (value === '20-25') return temp >= 20 && temp < 25;
      if (value === '25-30') return temp >= 25 && temp < 30;
      return true;
    },
  },
  {
    title: 'Humidity',
    dataIndex: 'humidity',
    sorter: (a, b) => a.humidity - b.humidity, // Sắp xếp theo Độ ẩm
    filters: [
      { text: '50% - 60%', value: '50-60' },
      { text: '60% - 70%', value: '60-70' },
    ],
    onFilter: (value, record) => {
      const humidity = parseFloat(record.humidity);
      if (value === '50-60') return humidity >= 50 && humidity < 60;
      if (value === '60-70') return humidity >= 60 && humidity < 70;
      return true;
    },
  },
  {
    title: 'Light',
    dataIndex: 'light',
    sorter: (a, b) => a.light - b.light, // Sắp xếp theo Ánh sáng
    filters: [
      { text: '0 - 50 lux', value: '0-50' },
      { text: '50 - 100 lux', value: '50-100' },
    ],
    onFilter: (value, record) => {
      const light = parseFloat(record.light);
      if (value === '0-50') return light >= 0 && light < 50;
      if (value === '50-100') return light >= 50 && light < 100;
      return true;
    },
  },
  {
    title: 'Time',
    dataIndex: 'time',
    sorter: (a, b) => new Date(a.time) - new Date(b.time),
  },
];

const TableSensors = () => {
  const [data, setData] = useState([]);  // Khởi tạo state cho dữ liệu thực
  const [loading, setLoading] = useState(false);  // Trạng thái tải dữ liệu
  const [tableParams, setTableParams] = useState({
    pagination: {
      current: 1,
      pageSize: 10,  // Số lượng bản ghi mỗi trang mặc định
      showSizeChanger: true, // Hiển thị tùy chọn chọn số lượng bản ghi mỗi trang
      pageSizeOptions: ['5', '10', '20', '50'], // Các tùy chọn số lượng bản ghi mỗi trang
      total: 0, // Số lượng bản ghi ban đầu là 0
    },
  });

  // Hàm fetch dữ liệu từ API
  const fetchData = async () => {
    setLoading(true);  // Bắt đầu tải dữ liệu
    try {
      const response = await fetch('http://localhost:5000/api/sensor_data');// URL của API
      const result = await response.json();  // Parse kết quả JSON
      console.log(result);
      setData(result);  // Cập nhật dữ liệu vào state
      setTableParams({
        ...tableParams,
        pagination: {
          ...tableParams.pagination,
          total: result.length,  // Cập nhật tổng số lượng bản ghi
        },
      });
    } catch (error) {
      message.error('Lỗi khi tải dữ liệu!');  // Hiển thị thông báo lỗi
    } finally {
      setLoading(false);  // Kết thúc tải dữ liệu
    }
  };

  // Sử dụng useEffect để gọi fetchData khi component mount
  useEffect(() => {
    fetchData();
  }, []);  // Chỉ gọi một lần khi component render lần đầu

  const handleTableChange = (pagination, filters, sorter) => {
    const filteredData = data
      .filter(item => {
        for (let key in filters) {
          if (filters[key] && filters[key].length > 0) {
            const filterFunc = columns.find(col => col.dataIndex === key).onFilter;
            if (!filters[key].some(val => filterFunc(val, item))) {
              return false;
            }
          }
        }
        return true;
      })
      .sort((a, b) => {
        if (!sorter.order) {
          return 0;
        }
        const compareFunc = columns.find(col => col.dataIndex === sorter.field).sorter;
        const compareResult = compareFunc(a, b);
        return sorter.order === 'ascend' ? compareResult : -compareResult;
      });

    setTableParams({
      pagination: {
        ...pagination,
        total: filteredData.length,  // Cập nhật số lượng bản ghi sau khi lọc
      },
      filters,
      sorter,
    });

    setData(filteredData.slice((pagination.current - 1) * pagination.pageSize, pagination.current * pagination.pageSize));
  };

  const onSearch = (value) => {
    const filteredData = data.filter(item =>
      item.time.includes(value)
    );
    setData(filteredData);
    setTableParams({
      ...tableParams,
      pagination: {
        ...tableParams.pagination,
        total: filteredData.length, // Cập nhật số lượng bản ghi sau khi tìm kiếm
      },
    });
  };

  return (
    <div className='dataSensors'>
      <div className='search'>
        <Search
          placeholder="Tìm kiếm theo thời gian"
          onSearch={onSearch}
          style={{
            width: 200,
          }}
        />
      </div>
      <div className='tableData'>
        <Table
          columns={columns}
          rowKey="id"
          dataSource={data}
          loading={loading}  // Trạng thái tải
          pagination={tableParams.pagination}
          onChange={handleTableChange}
          scroll={{ y: 400 }}
        />
      </div>
    </div>
  );
};

export default TableSensors;
