import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import VoltarButton from '../../components/VoltarButton';

function AdicionarPedido() {
  const { id: comandaId } = useParams();
  const [produtos, setProdutos] = useState([]);
  const [comanda, setComanda] = useState(null);
  const navigate = useNavigate();

  // Buscar produtos
  useEffect(() => {
    async function fetchProdutos() {
      try {
        const response = await api.get('/products');
        setProdutos(response.data);
      } catch (error) {
        console.error('Erro ao buscar produtos:', error);
      }
    }

    fetchProdutos();
  }, []);

  // Buscar status da comanda
  useEffect(() => {
    async function fetchComanda() {
      try {
        const response = await api.get(`/comandas/${comandaId}`);
        setComanda(response.data);
      } catch (error) {
        console.error('Erro ao buscar comanda:', error);
      }
    }

    fetchComanda();
  }, [comandaId]);

  const handleAdicionarProduto = async (produtoId) => {
    try {
      if (comanda?.status === 'fechada') {
        alert('Comanda fechada! Não é possível adicionar pedidos.');
        return;
      }

      await api.post(`/comandas/${comandaId}/pedidos`, {
        produto_id: produtoId,
        quantidade: 1
      });

      alert('Produto adicionado à comanda!');
      navigate(`/comandas/${comandaId}/pedidos`);
    } catch (error) {
      console.error('Erro ao adicionar produto:', error);
      alert('Erro ao adicionar produto.');
    }
  };

  return (
    <div className="container">
      <h2>Adicionar Pedido - Comanda #{comandaId}</h2>
      <VoltarButton />

      {comanda && comanda.status === 'fechada' && (
        <p style={{ color: 'red', fontWeight: 'bold' }}>
          Esta comanda está fechada. Não é possível adicionar produtos.
        </p>
      )}

      <table>
        <thead>
          <tr>
            <th>Produto</th>
            <th>Preço</th>
            <th>Estoque</th>
          </tr>
        </thead>
        <tbody>
          {produtos.length > 0 ? (
            produtos.map((produto) => (
              <tr
                key={produto.id}
                onClick={() => handleAdicionarProduto(produto.id)}
                style={{ cursor: comanda?.status !== 'fechada' ? 'pointer' : 'not-allowed', opacity: comanda?.status === 'fechada' ? 0.6 : 1 }}
              >
                <td>{produto.name}</td>
                <td>{produto.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                <td>{produto.stock}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3">Nenhum produto encontrado</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default AdicionarPedido;
