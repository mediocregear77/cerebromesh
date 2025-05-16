// File: dx_core_ui/components/ReplayExplain.jsx

import React, { useState } from 'react';
import './ReplayExplain.css';

function ReplayExplain({ decisionLog = [] }) {
  const [selectedId, setSelectedId] = useState(null);

  const selected = decisionLog.find(log => log.log_id === selectedId);

  return (
    <div className="replay-explain">
      <h3>🔍 Agent Decision Replay</h3>
      <div className="log-list">
        <ul>
          {decisionLog.map((log) => (
            <li key={log.log_id}>
              <button onClick={() => setSelectedId(log.log_id)}>
                {new Date(log.timestamp * 1000).toLocaleString()} — {log.action?.type || 'unknown'}
              </button>
            </li>
          ))}
        </ul>
      </div>

      {selected && (
        <div className="explain-box">
          <h4>🧠 Decision Details</h4>
          <p><strong>Agent ID:</strong> {selected.agent_id}</p>
          <p><strong>Action Type:</strong> {selected.action?.type}</p>
          <p><strong>Path:</strong> {selected.action?.path}</p>
          <p><strong>Method:</strong> {selected.action?.method}</p>
          <p><strong>Confidence:</strong> {selected.action?.confidence || 'N/A'}</p>
          <p><strong>Allowed:</strong> {selected.allowed ? '✅ Yes' : '⛔ No'}</p>
        </div>
      )}
    </div>
  );
}

export default ReplayExplain;
