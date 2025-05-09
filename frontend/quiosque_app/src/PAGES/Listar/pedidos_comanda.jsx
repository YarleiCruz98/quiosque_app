import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import './pedidos_comanda.css';
import VoltarButton from '../../components/VoltarButton';

function ComandaPedidos() {
  const { comandaId } = useParams();
  const [pedidos, setPedidos] = useState([]);
  const [mesa, setMesa] = useState(null);
  const [subtotal, setSubtotal] = useState(0); // faltando pagar
  const [subtotalOriginal, setSubtotalOriginal] = useState(0);
  const [totalPago, setTotalPago] = useState(0);
  const [status, setStatus] = useState('');
  const [valorPago, setValorPago] = useState('');
  const [troco, setTroco] = useState(null);

  useEffect(() => {
    async function fetchPedidos() {
      try {
        const response = await api.get(`/comandas/${comandaId}/pedidos`);
        const data = response.data;
        const chaveComanda = Object.keys(data)[0];
        const dadosComanda = data[chaveComanda];

        setPedidos(dadosComanda.pedidos);
        setMesa(dadosComanda.mesa);
        setSubtotal(dadosComanda.faltando_pagar || 0);
        setSubtotalOriginal(dadosComanda.subtotal_original || 0);
        setTotalPago(dadosComanda.total_pago || 0);
        setStatus(dadosComanda.status);
      } catch (error) {
        console.error("Erro ao buscar pedidos:", error);
      }
    }

    fetchPedidos();
  }, [comandaId]);

  async function handlePagamento() {
    try {
      const response = await api.post(`/comandas/${comandaId}/pagar`, {
        valor_pago: parseFloat(valorPago)
      });

      setTroco(response.data.troco);
      setStatus(response.data.status);
      setSubtotal(response.data.faltando_pagar);
      setSubtotalOriginal(response.data.subtotal_original);
      setTotalPago(response.data.total_pago);

      alert('Pagamento registrado com sucesso!');
    } catch (error) {
      console.error("Erro ao processar pagamento:", error);
      alert('Erro ao processar pagamento. Verifique o valor informado.');
    }
  }

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

      setStatus(response.data.status);
    } catch (error) {
      console.error(`Erro ao ${acao} comanda:`, error);
    }
  }

  return (
    <div className="container">
      <h2>Pedidos da Comanda #{comandaId}</h2>
      <VoltarButton />
      <p><strong>Mesa:</strong> {mesa}</p>
      <p><strong>Status:</strong> {status}</p>
      <p><strong>Subtotal original:</strong> R$ {subtotalOriginal.toFixed(2)}</p>
      <p><strong>Total já pago:</strong> R$ {totalPago.toFixed(2)}</p>
      <p><strong>Faltando pagar:</strong> R$ {subtotal.toFixed(2)}</p>

      {status === 'aberta' && (
        <div style={{ marginTop: '20px', marginBottom: '20px' }}>
          <label htmlFor="valorPago"><strong>Valor Pago:</strong></label>
          <input
            type="number"
            id="valorPago"
            step="0.01"
            min="0"
            value={valorPago}
            onChange={(e) => setValorPago(e.target.value)}
            placeholder="Digite o valor recebido"
            style={{ marginLeft: "10px", padding: "5px" }}
          />
          <button
            onClick={handlePagamento}
            disabled={isNaN(parseFloat(valorPago)) || parseFloat(valorPago) <= 0}
            style={{ marginLeft: "10px" }}
          >
            Confirmar Pagamento
          </button>
        </div>
      )}

      {troco !== null && (
        <p><strong>Troco:</strong> R$ {troco.toFixed(2)}</p>
      )}

      {status === 'aberta' && (
        <div style={{ marginBottom: "20px" }}>
          <button
            onClick={() => atualizarStatusComanda("fechar")}
            style={{ marginRight: "10px" }}
          >
            Fechar Comanda
          </button>
        </div>
      )}

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
