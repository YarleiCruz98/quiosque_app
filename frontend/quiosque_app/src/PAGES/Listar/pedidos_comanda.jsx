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

  useEffect(() => {
    async function fetchPedidos() {
      try {
        const response = await api.get(`/comandas/${comandaId}/pedidos`);
        const data = response.data;
        console.log("Dados da comanda:", data);

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

  async function atualizarStatusComanda(acao) {
    try {
      const statusMap = {
        fechar: "fechada",
        cancelar: "cancelada"
      };
  
      const status = statusMap[acao];
  
      if (!status) {
        console.error(`Ação inválida: ${acao}`);
        return;
      }
  
      const response = await api.post(`/comandas/${comandaId}/${acao}`, {
        status: status
      });
  
      console.log(`Comanda ${acao}:`, response.data);
  
      // Atualiza corretamente o status retornado
      setStatus(response.data.status); // ou .comanda.status dependendo da estrutura
    } catch (error) {
      console.error(`Erro ao ${acao} comanda:`, error);
    }
  }

  return (
    <div className="container">
      <h2>Pedidos da Comanda #{comandaId}</h2>
      <p><strong>Mesa:</strong> {mesa}</p>
      <p><strong>Status:</strong> {status}</p>
      <p><strong>Subtotal:</strong> R$ {subtotal}</p>

      <div style={{ marginBottom: "20px" }}>
  <button
    onClick={() => atualizarStatusComanda("fechar")}
    disabled={status !== "aberta"}
    style={{ marginRight: "10px" }}
  >
    Fechar Comanda
  </button>
  
</div>

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