// File: dx_core_ui/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

import IndexPage from './pages/index.jsx';
import BuilderPage from './pages/builder.jsx';
import DocsPage from './pages/docs.jsx';

import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="top-nav">
          <ul>
            <li><Link to="/">🏠 Dashboard</Link></li>
            <li><Link to="/builder">🛠 Builder</Link></li>
            <li><Link to="/docs">📚 Docs</Link></li>
          </ul>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<IndexPage />} />
            <Route path="/builder" element={<BuilderPage />} />
            <Route path="/docs" element={<DocsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
