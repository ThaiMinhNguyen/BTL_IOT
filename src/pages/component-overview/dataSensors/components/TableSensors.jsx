import React, { useState, useEffect } from 'react';
import { Table, Input, message } from 'antd';

const { Search } = Input;

// Cấu trúc cột cho bảng
const columns = [
  {
    title: 'ID',
    dataIndex: '_id',
    sorter: (a, b) => a._id.localeCompare(b._id),
  },
  {
    title: 'Temperature',
    dataIndex: ['dht11', 'temperature'], // Truy cập giá trị lồng nhau
    sorter: (a, b) => a.dht11.temperature - b.dht11.temperature,
    filters: [
      { text: '20°C - 25°C', value: '20-25' },
      { text: '25°C - 30°C', value: '25-30' },
    ],
    onFilter: (value, record) => {
      const temp = record.dht11.temperature;
      if (value === '20-25') return temp >= 20 && temp < 25;
      if (value === '25-30') return temp >= 25 && temp < 30;
      return true;
    },
  },
  {
    title: 'Humidity',
    dataIndex: ['dht11', 'humidity'],
    sorter: (a, b) => a.dht11.humidity - b.dht11.humidity,
    filters: [
      { text: '50% - 60%', value: '50-60' },
      { text: '60% - 70%', value: '60-70' },
    ],
    onFilter: (value, record) => {
      const humidity = record.dht11.humidity;
      if (value === '50-60') return humidity >= 50 && humidity < 60;
      if (value === '60-70') return humidity >= 60 && humidity < 70;
      return true;
    },
  },
  {
    title: 'Light (Lux)',
    dataIndex: ['bh1750', 'lux'],
    sorter: (a, b) => a.bh1750.lux - b.bh1750.lux,
  },
  {
    title: 'TVOC (ppm)',
    dataIndex: ['mq135', 'tvocppm'],
    sorter: (a, b) => a.mq135.tvocppm - b.mq135.tvocppm,
  },
  {
    title: 'CO2 (ppm)',
    dataIndex: ['mq135', 'co2ppm'],
    sorter: (a, b) => a.mq135.co2ppm - b.mq135.co2ppm,
  },
  {
    title: 'Ethanol (ppm)',
    dataIndex: ['mq135', 'ethanolppm'],
    sorter: (a, b) => a.mq135.ethanolppm - b.mq135.ethanolppm,
  },
  {
    title: 'Timestamp',
    dataIndex: 'timestamp',
    sorter: (a, b) => a.timestamp - b.timestamp,
    render: (timestamp) => new Date(timestamp * 1000).toLocaleString(),
  },
];

const TableSensors = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tableParams, setTableParams] = useState({
    pagination: {
      current: 1,
      pageSize: 10,
      showSizeChanger: true,
      pageSizeOptions: ['5', '10', '20', '50'],
      total: 0,
    },
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/sensors/history');
      const result = await response.json();
      setData(result);
      setTableParams({
        ...tableParams,
        pagination: {
          ...tableParams.pagination,
          total: result.length,
        },
      });
    } catch (error) {
      message.error('Error fetching data!');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTableChange = (pagination, filters, sorter) => {
    setTableParams({
      pagination,
      filters,
      sorter,
    });
  };

  const onSearch = (value) => {
    const filteredData = data.filter((item) =>
      new Date(item.timestamp * 1000).toLocaleString().includes(value)
    );
    setData(filteredData);
    setTableParams({
      ...tableParams,
      pagination: {
        ...tableParams.pagination,
        total: filteredData.length,
      },
    });
  };

  return (
    <div>
      <Search
        placeholder="Search by time"
        onSearch={onSearch}
        style={{
          width: 200,
          marginBottom: '20px',
        }}
      />
      <Table
        columns={columns}
        rowKey="_id"
        dataSource={data}
        loading={loading}
        pagination={tableParams.pagination}
        onChange={handleTableChange}
        scroll={{ y: 400 }}
      />
    </div>
  );
};

export default TableSensors;
