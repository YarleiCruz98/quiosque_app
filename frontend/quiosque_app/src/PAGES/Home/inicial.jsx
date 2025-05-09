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

      <div className="menu">
        <button onClick={() => handleNavigate("/products")}>Ver Cardápio</button>
        <button onClick={() => handleNavigate("/products/criar")}>Cadastrar Produto</button>
        <button onClick={() => handleNavigate("/comandas")}>Listar Comandas</button>
        <button onClick={() => handleNavigate("/comandas/criar")}>Criar Comanda</button>
      </div>
    </div>
  );
}

export default Home;
