// import React, { useEffect, useState } from 'react';
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   Tooltip,
//   Legend,
//   CartesianGrid,
//   ResponsiveContainer,
// } from 'recharts';

// const LiveDataGraph = () => {
//   const [data, setData] = useState([]);
//   const [selectedLines, setSelectedLines] = useState({
//     ph: true,
//     temperature: true,
//     aquarium: true,
//     filterbak: true,
//   });

//   // Ophalen van historische data
//   const fetchData = async () => {
//     try {
//       const response = await fetch('/api/sensor-history'); // Zorg dat dit endpoint bestaat
//       const json = await response.json();
//       const formatted = json.map(entry => ({
//         ...entry,
//         timestamp: new Date(entry.timestamp).toLocaleTimeString(),
//       }));
//       setData(formatted);
//     } catch (error) {
//       console.error('Fout bij ophalen data:', error);
//     }
//   };

//   useEffect(() => {
//     fetchData();
//     const interval = setInterval(fetchData, 10000); // elke 10 sec refresh
//     return () => clearInterval(interval);
//   }, []);

//   const handleCheckboxChange = (e) => {
//     const { name, checked } = e.target;
//     setSelectedLines(prev => ({
//       ...prev,
//       [name]: checked,
//     }));
//   };

//   return (
//     <div className="p-4">
//       <h2 className="text-xl font-semibold mb-4">Sensorhistoriek (Live)</h2>

//       <div className="flex gap-4 mb-4">
//         <label><input type="checkbox" name="ph" checked={selectedLines.ph} onChange={handleCheckboxChange} /> pH</label>
//         <label><input type="checkbox" name="temperature" checked={selectedLines.temperature} onChange={handleCheckboxChange} /> Temperatuur</label>
//         <label><input type="checkbox" name="aquarium" checked={selectedLines.aquarium} onChange={handleCheckboxChange} /> Aquarium</label>
//         <label><input type="checkbox" name="filterbak" checked={selectedLines.filterbak} onChange={handleCheckboxChange} /> Filterbak</label>
//       </div>

//       <ResponsiveContainer width="100%" height={400}>
//         <LineChart data={data}>
//           <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
//           <XAxis dataKey="timestamp" />
//           <YAxis />
//           <Tooltip />
//           <Legend />
//           {selectedLines.ph && <Line type="monotone" dataKey="ph" stroke="#8884d8" name="pH-waarde" />}
//           {selectedLines.temperature && <Line type="monotone" dataKey="temperature" stroke="#82ca9d" name="Temperatuur (°C)" />}
//           {selectedLines.aquarium && <Line type="monotone" dataKey="aquarium_cm" stroke="#00bcd4" name="Aquarium (cm)" />}
//           {selectedLines.filterbak && <Line type="monotone" dataKey="filterbak_cm" stroke="#ff9800" name="Filterbak (cm)" />}
//         </LineChart>
//       </ResponsiveContainer>
//     </div>
//   );
// };

// export default LiveDataGraph;
import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';

const LiveDataGraph = ({ data }) => {
  const [selectedLines, setSelectedLines] = useState({
    ph: true,
    temperature: true,
    aquarium: true,
    filterbak: true,
  });

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setSelectedLines(prev => ({
      ...prev,
      [name]: checked,
    }));
  };

  return (
    <div className="p-4">
      <div className="flex gap-4 mb-4">
        <label><input type="checkbox" name="ph" checked={selectedLines.ph} onChange={handleCheckboxChange} /> pH</label>
        <label><input type="checkbox" name="temperature" checked={selectedLines.temperature} onChange={handleCheckboxChange} /> Temperatuur</label>
        <label><input type="checkbox" name="aquarium" checked={selectedLines.aquarium} onChange={handleCheckboxChange} /> Aquarium</label>
        <label><input type="checkbox" name="filterbak" checked={selectedLines.filterbak} onChange={handleCheckboxChange} /> Filterbak</label>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          {selectedLines.ph && <Line type="monotone" dataKey="ph" stroke="#8884d8" name="pH-waarde" />}
          {selectedLines.temperature && <Line type="monotone" dataKey="temperature" stroke="#82ca9d" name="Temperatuur (°C)" />}
          {selectedLines.aquarium && <Line type="monotone" dataKey="aquarium_cm" stroke="#00bcd4" name="Aquarium (cm)" />}
          {selectedLines.filterbak && <Line type="monotone" dataKey="filterbak_cm" stroke="#ff9800" name="Filterbak (cm)" />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LiveDataGraph;
