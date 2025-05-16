// File: dx_core_ui/pages/builder.jsx

import React, { useState } from 'react';
import DragCanvas from '../components/DragCanvas';
import NLPromptInput from '../components/NLPromptInput';
import './builder.css';

function BuilderPage() {
  const [apiPlan, setApiPlan] = useState(null);

  const handlePromptResult = (result) => {
    setApiPlan(result);
  };

  return (
    <div className="builder-page">
      <header>
        <h2>🛠 API Builder</h2>
        <p>Design your API visually or describe it in plain language.</p>
      </header>

      <section className="nl-builder-box">
        <NLPromptInput onSubmit={handlePromptResult} />
      </section>

      <section className="canvas-section">
        <DragCanvas />
      </section>

      {apiPlan && (
        <section className="api-preview">
          <h3>📄 API Plan Summary</h3>
          <ul>
            {apiPlan.endpoints.map((ep, i) => (
              <li key={i}><strong>{ep.method}</strong> {ep.path} — {ep.description}</li>
            ))}
          </ul>
          <p><em>{apiPlan.reasoning}</em></p>
        </section>
      )}
    </div>
  );
}

export default BuilderPage;
