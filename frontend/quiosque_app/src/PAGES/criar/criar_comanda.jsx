import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import './comandaform.css';
import VoltarButton from '../../components/VoltarButton';
function ComandaForm() {

  const [formData, setFormData] = useState({
    mesa: '',
    data_abertura: '',
    status: 'aberta'
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};

    if (!formData.mesa) {
      newErrors.mesa = 'O número da mesa é obrigatório.';
    } else if (isNaN(formData.mesa) || formData.mesa <= 0) {
      newErrors.mesa = 'A mesa deve ser um número maior que zero.';
    }

    if (!formData.data_abertura) {
      newErrors.data_abertura = 'A data de abertura é obrigatória.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      alert('Por favor, corrija os erros no formulário.');
      return;
    }

    try {
      await api.post('/comandas/criar', {
        mesa: parseInt(formData.mesa),
        data_abertura: formData.data_abertura,
        status: formData.status
      });

      alert('Comanda criada com sucesso!');
      navigate('/comandas'); // redireciona para listagem ou outra página
    } catch (error) {
      console.error('Erro ao abrir comanda:', error);
      alert('Erro ao abrir comanda.');
    }
  };

  return (
    <div className="comanda-form">
      <h2>Abrir Nova Comanda</h2>
      <VoltarButton />
      <form onSubmit={handleSubmit}>
        <div>
          <label>Mesa:</label>
          <input
            type="number"
            name="mesa"
            value={formData.mesa}
            onChange={handleChange}
            required
          />
          {errors.mesa && <span className="error">{errors.mesa}</span>}
        </div>

        <div>
          <label>Data de Abertura:</label>
          <input
            type="datetime-local"
            name="data_abertura"
            value={formData.data_abertura}
            onChange={handleChange}
            required
          />
          {errors.data_abertura && (
            <span className="error">{errors.data_abertura}</span>
          )}
        </div>

        <button type="submit">Abrir Comanda</button>
      </form>
    </div>
  );
  
}

export default ComandaForm;
