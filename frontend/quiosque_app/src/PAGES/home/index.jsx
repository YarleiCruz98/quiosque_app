import React, { useState, useEffect } from 'react';
import api from '../../services/api'; // Supondo que você tenha um arquivo `api.js` configurado para fazer chamadas à API
import { useNavigate } from 'react-router-dom';


function ProductTable() {
  const [products, setProducts] = useState([]);
  const navigate = useNavigate(); // Para navegação entre páginas

  // Função para buscar a lista de produtos
  async function fetchProducts() {
    const products = await api.get('/products');
    setProducts(products.data);
  }

  useEffect(() => {
    fetchProducts();
  }, []);

  // Função para excluir um produto
  const handleDeleteProduct = async (id) => {
    if (window.confirm("Tem certeza de que deseja excluir este produto?")) {
      try {
        await api.delete(`/products/${id}/delete`);
        // Remove o produto da lista de produtos após a exclusão
        setProducts(products.filter(product => product.id !== id));
        alert('Produto excluído com sucesso!');
      } catch (error) {
        console.error('Erro ao excluir produto:', error);
        alert('Erro ao excluir o produto.');
      }
    }
  };

  // Função para redirecionar para a página de atualização de produto
  const handleUpdateProduct = (id) => {
    navigate(`/products/${id}/atualizar`); // Redireciona para a página de atualização
  };

  return (
    <div className="product-table">
      <h2>Lista do Cardápio</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Preço</th>
            <th>Estoque</th>
            <th>Descrição</th>
            <th>Ações</th> {/* Coluna para ações (Excluir/Atualizar) */}
          </tr>
        </thead>
        <tbody>
          {products.length > 0 ? (
            products.map((product) => (
              <tr key={product.id}>
                <td>{product.id}</td>
                <td>{product.name}</td>
                <td>{product.price.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL',
                  })}</td>
                 <td>{`${product.stock} und`}</td>
                <td>{product.description || 'Sem descrição'}</td>
                <td>
                  <button onClick={() => handleUpdateProduct(product.id)}>
                    Atualizar
                  </button>
                  <button onClick={() => handleDeleteProduct(product.id)} style={{ marginLeft: '10px' }}>
                    Excluir
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6">Nenhum produto encontrado</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ProductTable;