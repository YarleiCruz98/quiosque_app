import React, { useState } from 'react';
import api from '../../services/api'; // Supondo que você tenha um arquivo `api.js` configurado para fazer chamadas à API
import './productform.css'
import { useNavigate } from 'react-router-dom';

function ProductForm({ onProductAdded }) {
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    stock: '',
    description: ''
  });
    const navigate = useNavigate();

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }

    if (!formData.price) {
      newErrors.price = 'Preço é obrigatório';
    } else if (isNaN(formData.price) || formData.price <= 0) {
      newErrors.price = 'Preço deve ser um número maior que zero';
    }

    if (!formData.stock) {
      newErrors.stock = 'Estoque é obrigatório';
    } else if (isNaN(formData.stock) || formData.stock < 0) {
      newErrors.stock = 'Estoque deve ser um número não negativo';
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
      alert('Por favor, corrija os erros no formulário antes de enviar.');
      return;
    }

    try {
      const response = await api.post('/products', formData);
      
      // Verifica se onProductAdded é uma função antes de chamar
      if (typeof onProductAdded === 'function') {
        onProductAdded(response.data);
      }

      setFormData({
        name: '',
        price: '',
        stock: '',
        description: ''
      });
      alert('Produto adicionado com sucesso!');
      navigate('/products'); // Redireciona para a página inicial
    } catch (error) {
      console.error('Erro ao adicionar produto:', error);
      alert('Erro ao adicionar produto.');
    }
  };

  return (
    <div className="product-form">
      <h2>Adicionar Novo Produto</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nome:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          {errors.name && <span className="error">{errors.name}</span>}
        </div>
        <div>
          <label>Preço:</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            required
          />
          {errors.price && <span className="error">{errors.price}</span>}
        </div>
        <div>
          <label>Estoque:</label>
          <input
            type="number"
            name="stock"
            value={formData.stock}
            onChange={handleChange}
            required
          />
          {errors.stock && <span className="error">{errors.stock}</span>}
        </div>
        <div>
          <label>Descrição:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Adicionar Produto</button>
      </form>
    </div>
  );
}

export default ProductForm;