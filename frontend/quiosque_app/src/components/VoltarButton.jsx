import React from 'react';
import { useNavigate } from 'react-router-dom';
import './VoltarButton.css';

function VoltarButton() {
  const navigate = useNavigate();

  return (
    <button className="voltar-button" onClick={() => navigate(-1)}>
      ← Voltar
    </button>
  );
}

export default VoltarButton;
