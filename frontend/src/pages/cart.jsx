import { useContext, useEffect } from 'react';
import { UserContext } from '../contexts/user_context';
import { CartContext } from '../contexts/cart_context';
import '../styles/cart.css'
import Navbar from '../components/navbar';
import Btn from '../components/btn';
import axios from 'axios';

export default function Cart() {
    const { isLoggedIn } = useContext(UserContext)
    const { cart, addToCart, removeFromCart, removeFromCartCompletely, setAllCart } = useContext(CartContext)
    const serverUrl = import.meta.env.VITE_SERVER_URL

    const onQuantityChange = async (item, operation) => {
        operation == 1 ? addToCart(item) : removeFromCart(item)
        try {
            const data = {
                mockup_id: item.id,
                quantity: item.quantity + operation
            }

            await axios.post(serverUrl + '/update-cart-item', data, {withCredentials: true})
        }
        catch (error){
            console.log(error)
        }
    }

    const onRemove = async (item) => {
        removeFromCartCompletely(item)
        try {
            const data = {
                mockup_id: item.id
            }

            await axios.post(serverUrl + '/delete-cart-item', data, {withCredentials: true})
        }
        catch (error){
            console.log(error)
        }
    }

    const ifLoggedIn = async () => {
        try {
            const response = await axios.get(serverUrl + '/get-user-cart', {withCredentials: true})
            console.log(response.data)
            setAllCart(response.data)
        }
        catch (error){
            console.log(error)
        }
    }

    useEffect(() => {
        console.log("adssada")
        console.log(isLoggedIn)
        if(isLoggedIn){
            console.log("labs")
            ifLoggedIn()
        }
    }, [])

    console.log(cart)

    return (
        <>
            <div className="container"> 
                <Navbar/>
                {cart.length > 0 ? (
                    <div className="cart-item-container">
                        <h1 className="cart-title">CART</h1>
                        {cart.map((item) => (
                             <div className="cart-item-card shadow">
                                <div className="cart-item-image-container">
                                    <img src={item.mockup_image_url} alt={item.title} className="cart-item-image" />
                                </div>
                                <div className="cart-item-details">
                                    <h3 className="cart-item-title">{item.title}</h3>
                                    <p className="cart-item-text"><strong>Size:</strong> {item.size}</p>
                                    <p className="cart-item-text"><strong>Color:</strong> {item.color}</p>
                                </div>
                                <div className="cart-item-actions">
                                    <p className="cart-item-price">${item.price.toFixed(2)}</p>
                                    <div className="cart-item-quantity-selector">
                                        <button className="cart-item-quantity-button" onClick={() => onQuantityChange(item, -1)} disabled={item.quantity <= 1}>-</button>
                                        <span>{item.quantity}</span>
                                        <button className="cart-item-quantity-button" onClick={() => onQuantityChange(item, 1)}>+</button>
                                    </div>
                                    <button className="cart-item-remove-button" onClick={() => onRemove(item)}>Remove</button>
                                </div>
                            </div>
                        ))}
                        <div className="checkout-btn-container">
                            <Btn value="CHECKOUT"/>
                        </div>
                    </div>
                ): (
                    <div className="empty-cart-container">
                        <h1 className="cart-empty-text">Your cart is empty</h1>
                    </div>
                )}

            </div>
        </>
    )
}
