import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import App from './App.jsx'
import Login from './pages/login.jsx'
import Register from './pages/register.jsx'
import ProductList from './pages/product_list.jsx'
import ProductInfo from './pages/product_info.jsx'
import Gallery from './pages/gallery.jsx'
import AuthenticateWait from './pages/authenticate_wait.jsx'
import MyGallery from './pages/mygallery.jsx'
import Cart from './pages/cart.jsx'
import Pay from './pages/pay.jsx'
import ThankYou from './pages/thank_you.jsx'
import './index.css'
import { UserProvider } from './contexts/user_context.jsx'
import { CartProvider } from './contexts/cart_context.jsx'

createRoot(document.getElementById('root')).render(
    <UserProvider>
      <CartProvider>
        <BrowserRouter>
          <Routes>
            <Route path='/' element={<App/>}/>
            <Route path='/login' element={<Login/>}/>
            <Route path='/register' element={<Register/>}/>
            <Route path='/product-list' element={<ProductList/>}/>
            <Route path='/product-info' element={<ProductInfo/>}/>
            <Route path='/gallery' element={<Gallery/>}/>
            <Route path='/my-gallery' element={<MyGallery/>}/>
            <Route path='/authenticate-wait' element={<AuthenticateWait/>}/>
            <Route path='/cart' element={<Cart/>}/>
            <Route path='/pay' element={<Pay/>}/>
            <Route path='/thank-you' element={<ThankYou/>}/>
          </Routes>
        </BrowserRouter>
      </CartProvider>
    </UserProvider>
)
