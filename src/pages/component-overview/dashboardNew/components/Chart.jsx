import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Chart = ({ data }) => {
  return (
    <LineChart width={600} height={400} data={data} 
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis yAxisId="left" />
      <YAxis yAxisId="right" orientation="right" />
      <Tooltip />
      <Legend />
      <Line yAxisId="left" type="monotone" dataKey="temperature" stroke="#8884d8" activeDot={{ r: 8 }} />
      <Line yAxisId="left" type="monotone" dataKey="humidity" stroke="#82ca9d" />
      <Line yAxisId="right" type="monotone" dataKey="light" stroke="#ffc658" />
    </LineChart>
  );
};

export default Chart;
