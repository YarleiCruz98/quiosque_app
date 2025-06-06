import React, { useEffect, useState } from "react";
import api from "../../services/api";
import "./pagamentos.css";
import VoltarButton from "../../components/VoltarButton";

function Pagamentos() {
  const [pagamentos, setPagamentos] = useState([]);

  useEffect(() => {
    async function fetchPagamentos() {
      try {
        const response = await api.get(`/comandas/hitorico/pagamento`);
        setPagamentos(response.data);
      } catch (error) {
        console.error("Erro ao buscar pagamentos:", error);
      }
    }

    fetchPagamentos();
  }, []);

  return (
    <div className="pagamentos-container">
      <VoltarButton />
      <h1>Pagamentos</h1>
      <table className="pagamentos-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Valor Pago</th>
            <th>Troco</th>
            <th>Data do Pagamento</th>
          </tr>
        </thead>
        <tbody>
          {pagamentos.map((pagamento) => (
            <tr key={pagamento.id}>
              <td>{pagamento.id}</td>
              <td>R$ {(pagamento.valor_pago ?? 0).toFixed(2)}</td>
              <td>R$ {(pagamento.troco ?? 0).toFixed(2)}</td>
              <td>
                {pagamento.data_pagamento
                  ? new Date(pagamento.data_pagamento).toLocaleDateString()
                  : 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Pagamentos;
