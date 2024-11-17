import React from 'react';
import { AudioOutlined } from '@ant-design/icons';
import { Input, Space } from 'antd';
const { Search } = Input;
import "./components/TableSensors"
import TableSensors from './components/TableSensors';
import "./dataSensors.scss";

function dataSensors() {
  return (
    <div className='dataSensors'>
        <div className='tableData'>
          <TableSensors />
        </div>
    </div>
  )
}

export default dataSensors
