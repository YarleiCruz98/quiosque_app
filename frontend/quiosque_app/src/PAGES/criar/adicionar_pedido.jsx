import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

function AdicionarPedido() {
  const { id: comandaId } = useParams(); // pega o ID da comanda da URL
  const [produtos, setProdutos] = useState([]);
  const navigate = useNavigate();

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

  const handleAdicionarProduto = async (produtoId) => {
    try {
      await api.post(`/comandas/${comandaId}/pedidos`, {
        produto_id: produtoId,
        quantidade: 1
      });
      alert('Produto adicionado à comanda!');
      navigate(`/comandas/${comandaId}/pedidos`); // redireciona de volta à comanda (se quiser)
    } catch (error) {
      console.error('Erro ao adicionar produto:', error);
      alert('Erro ao adicionar produto.');
    }
  };

  return (
    <div className="container">
      <h2>Adicionar Pedido - Comanda #{comandaId}</h2>
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
              <tr key={produto.id} onClick={() => handleAdicionarProduto(produto.id)} style={{ cursor: 'pointer' }}>
                <td>{produto.name}</td>
                <td>{produto.price.toLocaleString('pt-BR', {
                  style: 'currency',
                  currency: 'BRL',
                })}</td>
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
