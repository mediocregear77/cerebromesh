// File: dx_core_ui/components/TimelinePlayer.jsx

import React, { useEffect, useState } from 'react';
import './TimelinePlayer.css';

function TimelinePlayer({ events = [] }) {
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    let interval;
    if (playing && events.length > 0) {
      interval = setInterval(() => {
        setIndex(prev => (prev + 1 < events.length ? prev + 1 : prev));
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [playing, events]);

  const currentEvent = events[index] || {};

  return (
    <div className="timeline-player">
      <h3>🧠 Memory Mesh Timeline</h3>
      <div className="event-box">
        <p><strong>Event Type:</strong> {currentEvent.event_type}</p>
        <p><strong>Timestamp:</strong> {new Date(currentEvent.timestamp * 1000).toLocaleString()}</p>
        <pre>{JSON.stringify(currentEvent.data, null, 2)}</pre>
      </div>
      <div className="timeline-controls">
        <button onClick={() => setPlaying(!playing)}>
          {playing ? 'Pause' : 'Play'}
        </button>
        <button onClick={() => setIndex(index > 0 ? index - 1 : 0)}>⏮ Prev</button>
        <button onClick={() => setIndex(index + 1 < events.length ? index + 1 : index)}>⏭ Next</button>
        <span>Event {index + 1} of {events.length}</span>
      </div>
    </div>
  );
}

export default TimelinePlayer;
