# components.py
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const MetricsChart = ({ metrics }) => {
  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Ecommerce Metrics</CardTitle>
      </CardHeader>
      <CardContent>
        <BarChart width={800} height={400} data={metrics}>
          <XAxis dataKey="Métrique" />
          <YAxis type="number" domain={['dataMin', 'dataMax']} />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          <Bar dataKey="Valeur" fill="#8884d8" />
        </BarChart>
      </CardContent>
    </Card>
  );
};

export default MetricsChart;
