import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import './pedidos_comanda.css';

function ComandaPedidos() {
    const { comandaId } = useParams();
    const [pedidos, setPedidos] = useState([]);
    const [mesa, setMesa] = useState(null);
    const [subtotal, setSubtotal] = useState(0);
    const [status, setStatus] = useState('');
    console.log("Comanda ID:", comandaId);
    
    useEffect(() => {
      async function fetchPedidos() {
        try {
          const response = await api.get(`/comandas/${comandaId}/pedidos`);
          const data = response.data;
          console.log("Resposta da API:", response.data);
  
          // Pega a primeira chave do objeto (ex: "comanda-2")
          const chaveComanda = Object.keys(data)[0];
          const dadosComanda = data[chaveComanda];
  
          setPedidos(dadosComanda.pedidos);
          setMesa(dadosComanda.mesa);
          setSubtotal(dadosComanda.subtotal);
          setStatus(dadosComanda.status);
        } catch (error) {
          console.error("Erro ao buscar pedidos:", error);
        }
      }
  
      fetchPedidos();
    }, [comandaId]);
  
    return (
      <div className="container">
        <h2>Pedidos da Comanda #{comandaId}</h2>
        <p><strong>Mesa:</strong> {mesa}</p>
        <p><strong>Status:</strong> {status}</p>
        <p><strong>Subtotal:</strong> R$ {subtotal}</p>
  
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Produto</th>
              <th>Quantidade</th>
              <th>Preço Unitário</th>
              <th>Descrição</th>
            </tr>
          </thead>
          <tbody>
            {pedidos.length > 0 ? (
              pedidos.map((pedido) => (
                <tr key={pedido.pedido_id}>
                  <td>{pedido.pedido_id}</td>
                  <td>{pedido.nome_produto}</td>
                  <td>{pedido.quantidade}</td>
                  <td>R$ {pedido.preco_unitario.toFixed(2)}</td>
                  <td>{pedido.descricao || 'Sem observações'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">Nenhum pedido encontrado para esta comanda.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    );
  }
  
  export default ComandaPedidos;
