import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ProductTable from './PAGES/Listar/index' 
import ProductForm from './PAGES/criar/productform'
import ProductUpdateForm from './PAGES/update/updateform'
import Home from './PAGES/Home/inicial'
import ComandaTable from './PAGES/Listar/comandas' // Importa o componente ComandaTable
import AdicionarPedido from './PAGES/criar/adicionar_pedido'
import ComandaPedidos from './PAGES/Listar/pedidos_comanda' // Importa o componente PedidosComanda
import ComandaForm from './PAGES/criar/criar_comanda' // Importa o componente ComandaForm
import Pagamentos from './PAGES/Listar/pagamentos'

function App() {
  return (
    <Router>
      <Routes>
        {/* Rota para exibir a lista de produtos */}
        <Route path="/products" element={<ProductTable />} />
        {/* Rota para adicionar um novo produto */}
        <Route path="/products/criar" element={<ProductForm onProductAdded={() => {}} />}  />
        {/* Rota para atualizar um produto */}
        <Route path="products/:id/atualizar" element={<ProductUpdateForm onProductAdded={() => {}} />} />
        {/* Rota para a página inicial */}
        <Route path="/" element={<Home />} />
        {/* Rota para exibir a lista de comandas abertas */}
        <Route path="/comandas" element={<ComandaTable />} /> 
        {/* Adiciona a rota para ComandaTable */}
        <Route path="/comandas/:id/pedido" element={<AdicionarPedido />} />
        {/* Rota para exibir os pedidos de uma comanda específica */}
        <Route path="/comandas/:comandaId/pedidos" element={<ComandaPedidos />} />
        {/* Rota para criar uma nova comanda */}
        <Route path="/comandas/criar" element={<ComandaForm />} />
        {/* Rota para exibir os pagamentos de uma comanda específica */}
        <Route path="/comandas/pagamentos" element={<Pagamentos />} />
      </Routes>
    </Router>
  );
}

export default App;