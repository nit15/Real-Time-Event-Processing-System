import React, { useState, useEffect } from "react";
import axios from "axios";
import './Sensor_dashboard.css';


const Sensor_dashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get("http://localhost:8000/sensors");
      console.log("Fetched data:", result.data);
      setData(result.data.data);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Real-Time Sensor Data</h1>
      <table>
        <thead>
          <tr>
            <th>Sensor ID</th>
            <th>Value</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
  {data && data.map((row, index) => (
    <tr key={index}>
      <td>{row[0]}</td>
      <td>{row[1]}</td>
      <td>{row[2]}</td>
    </tr>
  ))}
</tbody>
      </table>
    </div>
  );
};

export default Sensor_dashboard;