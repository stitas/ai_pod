import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import App from './App.jsx'
import Login from './pages/login.jsx'
import Register from './pages/register.jsx'
import ProductList from './pages/product_list.jsx'
import ProductInfo from './pages/product_info.jsx'
import Gallery from './pages/gallery.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<App/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/register' element={<Register/>}/>
        <Route path='/product-list' element={<ProductList/>}/>
        <Route path='/product-info' element={<ProductInfo/>}/>
        <Route path='/gallery' element={<Gallery/>}/>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
