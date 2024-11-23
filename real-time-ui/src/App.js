import React from 'react';
import './App.css';
import Sensor_dashboard from './Sensor_dashboard'; // Import your SensorDashboard component

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the Real-Time Sensor Dashboard</h1>
      </header>
      <main>
        <Sensor_dashboard/> {/* Include the SensorDashboard component */}
      </main>
    </div>
  );
}

export default App;

