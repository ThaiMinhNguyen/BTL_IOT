import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const GasChart = ({ data }) => {
  return (
    <LineChart
      width={600}
      height={400}
      data={data}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="CO2" stroke="#FF5733" activeDot={{ r: 8 }} />
      <Line type="monotone" dataKey="CO" stroke="#33FF57" />
      <Line type="monotone" dataKey="TVOC" stroke="#3357FF" />
      <Line type="monotone" dataKey="Ethanol" stroke="#FF33A6" />
      <Line type="monotone" dataKey="SO2" stroke="#FFC300" />
      <Line type="monotone" dataKey="NO2" stroke="#00C3FF" />
    </LineChart>
  );
};

export default GasChart;
