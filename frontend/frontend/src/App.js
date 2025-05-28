// import React, { useEffect, useState } from 'react';
// import LiveDataGraph from './LiveDataGraph'; // <-- voeg deze regel toe

// function App() {
//   const [data, setData] = useState({});
//   const [status, setStatus] = useState('Disconnected');

//   useEffect(() => {
//     const socket = new WebSocket('ws://localhost:8000/ws/ac/');

//     socket.onopen = () => setStatus('Connected');
//     socket.onclose = () => setStatus('Disconnected');

//     socket.onmessage = (event) => {
//       const sensorData = JSON.parse(event.data);
//       setData(sensorData);
//     };

//     return () => socket.close();
//   }, []);

//   return (
//     <div style={{ textAlign: 'center', paddingTop: '2rem', paddingBottom: '4rem' }}>
//       <h1>📡 Realtime Sensor Dashboard</h1>
//       <h2>Status: {status}</h2>

//       {data.ph !== undefined && (
//         <p>💧 pH-Waarde: {data.ph}</p>
//       )}

//       {data.temperature !== undefined && (
//         <p>🌡️ Temperatuur: {data.temperature} °C</p>
//       )}

//       {data.water_levels && (
//         <>
//           {data.water_levels.aquarium ? (
//             <>
//               <h3>Aquarium</h3>
//               <p>🌡️ Waterniveau: {data.water_levels.aquarium.percentage}%</p>
//               <p>📏 Waterhoogte: {data.water_levels.aquarium.cm} cm</p>
//             </>
//           ) : (
//             <p>Aquarium waterniveau: niet beschikbaar</p>
//           )}

//           {data.water_levels.filterbak ? (
//             <>
//               <h3>Filterbak</h3>
//               <p>🌡️ Waterniveau: {data.water_levels.filterbak.percentage}%</p>
//               <p>📏 Waterhoogte: {data.water_levels.filterbak.cm} cm</p>
//             </>
//           ) : (
//             <p>Filterbak waterniveau: niet beschikbaar</p>
//           )}
//         </>
//       )}

//       {(!data.ph || !data.temperature || !data.water_levels) && (
//         <p>Wachten op data...</p>
//       )}

//       {/* === GRAFIEK HIERONDER === */}
//       <div style={{ marginTop: '3rem' }}>
//         <h2>📈 Historiek Sensorwaarden</h2>
//         <LiveDataGraph />
//       </div>
//     </div>
//   );
// }

// export default App;
import React, { useEffect, useState } from 'react';
import LiveDataGraph from './LiveDataGraph';

function App() {
  const [data, setData] = useState({});
  const [status, setStatus] = useState('Disconnected');
  const [history, setHistory] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/ac/');

    socket.onopen = () => setStatus('Connected');
    socket.onclose = () => setStatus('Disconnected');

    socket.onmessage = (event) => {
      const sensorData = JSON.parse(event.data);
      setData(sensorData);
    };

    return () => socket.close();
  }, []);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/sensor-history/');
        const json = await res.json();

        const formatted = json.map(entry => ({
          ...entry,
          timestamp: entry.timestamp,
          aquarium_cm: entry.water_level_aquarium_cm,
          filterbak_cm: entry.water_level_filterbak_cm,
        }));

        setHistory(formatted);
      } catch (err) {
        console.error('Fout bij laden historiek:', err);
      }
    };

    fetchHistory();
  }, []);

  // 🔍 Filter data op geselecteerde datum
  const filteredHistory = selectedDate
    ? history.filter(entry =>
        entry.timestamp.startsWith(selectedDate)
      )
    : history;

  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      <h1>📡 Realtime Sensor Dashboard</h1>
      <h2>Status: {status}</h2>

      {data.ph !== undefined && (
        <div>
          <p>💧 pH-Waarde: {data.ph}</p>
          <p>🌡️ Temperatuur: {data.temperature} °C</p>
          {data.water_levels && (
            <>
              <h3>Aquarium</h3>
              <p>📏 Waterhoogte: {data.water_levels.aquarium.cm} cm</p>
              <h3>Filterbak</h3>
              <p>📏 Waterhoogte: {data.water_levels.filterbak.cm} cm</p>
            </>
          )}
        </div>
      )}

      {/* Datumfilter */}
      <div style={{ marginTop: '2rem' }}>
        <label htmlFor="date">📅 Kies een datum:</label>{' '}
        <input
          id="date"
          type="date"
          value={selectedDate}
          onChange={e => setSelectedDate(e.target.value)}
        />
      </div>

      {/* Grafiek */}
      <div style={{ marginTop: '2rem' }}>
        <h2>📈 Historiek Sensorwaarden</h2>
        {filteredHistory.length > 0 ? (
          <LiveDataGraph data={filteredHistory} />
        ) : (
          <p>❗ Geen data gevonden voor deze datum.</p>
        )}
      </div>
    </div>
  );
}

export default App;

