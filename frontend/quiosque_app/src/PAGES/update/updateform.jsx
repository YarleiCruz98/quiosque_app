import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import './updateform.css';

function UpdateProductForm() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: '',
    price: '',
    stock: '',
    description: ''
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await api.get(`/products/${id}`);
        setFormData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Erro ao carregar o produto:', error);
        setError('Erro ao carregar os dados do produto');
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validação dos campos obrigatórios
    if (!formData.name || !formData.price || !formData.stock) {
      setError('Preencha todos os campos obrigatórios.');
      return;
    }

    try {
      await api.put(`/products/${id}/atualizar`, formData);
      setSuccess('Produto atualizado com sucesso!');
      setTimeout(() => {
        navigate('/products'); // Redireciona para a página inicial após 2 segundos
      }, 2000);
    } catch (error) {
      console.error('Erro ao atualizar produto:', error);
      setError('Erro ao atualizar o produto.');
    }
  };

  if (loading) {
    return <div>Carregando dados do produto...</div>;
  }

  return (
    <div className="product-form-update">
      <h2>Atualizar Produto</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nome:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>
        <div>
          <label>Preço:</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: e.target.value })}
            required
          />
        </div>
        <div>
          <label>Estoque:</label>
          <input
            type="number"
            name="stock"
            value={formData.stock}
            onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
            required
          />
        </div>
        <div>
          <label>Descrição:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          />
        </div>
        <button type="submit">Atualizar Produto</button>
      </form>
    </div>
  );
}

export default UpdateProductForm;