// File: dx_core_ui/components/DragCanvas.jsx

import React, { useState } from 'react';
import './DragCanvas.css';

const initialElements = [
  { id: '1', label: 'GET /items', type: 'GET', x: 100, y: 100 },
  { id: '2', label: 'POST /orders', type: 'POST', x: 300, y: 200 },
];

function DragCanvas() {
  const [elements, setElements] = useState(initialElements);
  const [dragging, setDragging] = useState(null);

  const handleMouseDown = (e, id) => {
    e.preventDefault();
    setDragging({ id, offsetX: e.clientX, offsetY: e.clientY });
  };

  const handleMouseMove = (e) => {
    if (!dragging) return;
    const { id, offsetX, offsetY } = dragging;
    const deltaX = e.clientX - offsetX;
    const deltaY = e.clientY - offsetY;

    setElements(prev =>
      prev.map(el =>
        el.id === id ? { ...el, x: el.x + deltaX, y: el.y + deltaY } : el
      )
    );

    setDragging({ id, offsetX: e.clientX, offsetY: e.clientY });
  };

  const handleMouseUp = () => {
    setDragging(null);
  };

  return (
    <div
      className="drag-canvas"
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      {elements.map(el => (
        <div
          key={el.id}
          className={`drag-box ${el.type.toLowerCase()}`}
          style={{ top: el.y, left: el.x }}
          onMouseDown={(e) => handleMouseDown(e, el.id)}
        >
          {el.label}
        </div>
      ))}
    </div>
  );
}

export default DragCanvas;
