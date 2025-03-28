import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ProductTable from './PAGES/Listar/index' 
import ProductForm from './PAGES/criar/productform'
import ProductUpdateForm from './PAGES/update/updateform'
import Home from './PAGES/Home/inicial'

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
      </Routes>
    </Router>
  );
}

export default App;