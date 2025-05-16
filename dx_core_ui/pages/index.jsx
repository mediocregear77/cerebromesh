// File: dx_core_ui/pages/index.jsx

import React from 'react';
import DragCanvas from '../components/DragCanvas';
import NLPromptInput from '../components/NLPromptInput';
import TimelinePlayer from '../components/TimelinePlayer';
import ReplayExplain from '../components/ReplayExplain';
import './index.css';

// Dummy data for demo purposes
const sampleEvents = [
  {
    event_type: "route_created",
    timestamp: Math.floor(Date.now() / 1000) - 60,
    data: { path: "/checkout", method: "POST", description: "Processes user checkout" },
    tags: ["ecommerce", "checkout"]
  },
  {
    event_type: "test_passed",
    timestamp: Math.floor(Date.now() / 1000),
    data: { path: "/checkout", status: "200 OK" },
    tags: ["test", "success"]
  }
];

const sampleDecisions = [
  {
    log_id: "a1b2c3",
    timestamp: Math.floor(Date.now() / 1000) - 45,
    agent_id: "agent-001",
    action: { type: "route_add", path: "/checkout", method: "POST", confidence: 0.94 },
    allowed: true
  },
  {
    log_id: "d4e5f6",
    timestamp: Math.floor(Date.now() / 1000) - 10,
    agent_id: "agent-002",
    action: { type: "modify", path: "/cart", method: "GET", confidence: 0.58 },
    allowed: false
  }
];

function IndexPage() {
  const handlePromptResult = (result) => {
    console.log("Prompt Result:", result);
    // Future: trigger memory mesh event logging or dynamic canvas update
  };

  return (
    <div className="index-page">
      <header>
        <h1>🧬 CerebroMesh</h1>
        <p>The API that evolves, explains, and defends itself.</p>
      </header>

      <section>
        <NLPromptInput onSubmit={handlePromptResult} />
      </section>

      <section>
        <DragCanvas />
      </section>

      <section>
        <TimelinePlayer events={sampleEvents} />
      </section>

      <section>
        <ReplayExplain decisionLog={sampleDecisions} />
      </section>
    </div>
  );
}

export default IndexPage;
