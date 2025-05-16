// File: dx_core_ui/components/NLPromptInput.jsx

import React, { useState } from 'react';
import './NLPromptInput.css';

function NLPromptInput({ onSubmit }) {
  const [prompt, setPrompt] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [response, setResponse] = useState(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    setIsSubmitting(true);
    try {
      // Simulate backend call
      const fakeResponse = {
        endpoints: [
          { path: "/checkout", method: "POST", description: "Processes a user checkout" },
          { path: "/cart", method: "GET", description: "Returns items in cart" },
        ],
        reasoning: "Detected e-commerce pattern based on keywords: 'checkout', 'cart'"
      };
      setTimeout(() => {
        setResponse(fakeResponse);
        onSubmit && onSubmit(fakeResponse);
        setIsSubmitting(false);
      }, 1000);
    } catch (err) {
      console.error("Error:", err);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="nl-prompt-input">
      <h3>🧠 Describe your API</h3>
      <textarea
        placeholder="e.g., I want an API to let users view products, add to cart, and check out"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={handleSubmit} disabled={isSubmitting}>
        {isSubmitting ? 'Generating...' : 'Generate API'}
      </button>

      {response && (
        <div className="nl-response-box">
          <h4>✅ Suggested Endpoints:</h4>
          <ul>
            {response.endpoints.map((ep, i) => (
              <li key={i}><strong>{ep.method}</strong> {ep.path} — {ep.description}</li>
            ))}
          </ul>
          <p><em>Reasoning:</em> {response.reasoning}</p>
        </div>
      )}
    </div>
  );
}

export default NLPromptInput;
