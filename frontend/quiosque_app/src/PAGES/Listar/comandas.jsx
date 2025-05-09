import React, { useState, useEffect } from 'react';
import api from '../../services/api'; // Arquivo de configuração da API
import { useNavigate } from 'react-router-dom';
import './comandas.css'; // Estilos para a tabela de comandas
import VoltarButton from '../../components/VoltarButton';

function ComandaTable() {
  const [comandas, setComandas] = useState([]);
  const navigate = useNavigate();

  // Buscar as comandas abertas
  async function fetchComandas() {
    try {
      const response = await api.get('/comandas'); // Ajuste a rota conforme necessário
      setComandas(response.data);
    } catch (error) {
      console.error('Erro ao buscar comandas:', error);
    }
  }

  useEffect(() => {
    fetchComandas();
  }, []);

  // Função para visualizar detalhes da comanda
  const handleViewComanda = (id) => {
    navigate(`/comandas/${id}/pedidos`); // Redireciona para os detalhes da comanda
  };

  return (
    <div className="comanda-table">
      <h2>Comandas Abertas</h2>
      <VoltarButton />
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Número da Mesa</th>
            <th>Data de Abertura</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {comandas.length > 0 ? (
            comandas.map((comanda) => (
              <tr key={comanda.id}>
                <td>{comanda.id}</td>
                <td>{comanda.mesa}</td>
                <td>{new Date(comanda.data_abertura).toLocaleString('pt-BR')}</td>
                <td>
                  <button onClick={() => handleViewComanda(comanda.id)}>
                    Visualizar
                  </button>
                  <button onClick={() => navigate(`/comandas/${comanda.id}/pedido`)}>
                    Adicionar Pedido
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4">Nenhuma comanda aberta encontrada</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ComandaTable;
