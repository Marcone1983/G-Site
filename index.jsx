import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app.jsx';
import './app.css'; // Importa il CSS per Tailwind

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
