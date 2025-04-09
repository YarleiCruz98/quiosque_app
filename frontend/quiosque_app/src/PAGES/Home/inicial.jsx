import React from "react";
import { useNavigate } from "react-router-dom";
import "./inicial.css";

function Home() {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="home">
      <h1>Seja bem-vindo ao Quiosque Areia Sereia!</h1>
      <button onClick={() => handleNavigate("/products")}>
        Ver Cardápio
      </button>
    </div>
  );
}

export default Home;