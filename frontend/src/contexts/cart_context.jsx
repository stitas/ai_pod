import React, { createContext, useState, useEffect } from 'react';

// Create the UserContext
export const CartContext = createContext();

// UserProvider component to wrap around the application
export const CartProvider = ({ children }) => {
    const[cart, setCart] = useState([])

    const addToCart = (item) => {
        if(cart.includes(item, 0)){
            const index = cart.findIndex(item)
            const item_id = cart[index].id
            setCart(() => cart.map(
                (item) => {
                    item.id == item_id ? {...item, quantity: item.quantity + 1} : item
                }
            ))
        }
        else {
            setCart(() => [...cart, {...item, quantity: 1}])
        }
        
    }

    const removeFromCart = (item) => {
        const index = cart.findIndex(item)

        if(cart[index].quantity === 1){
            setCart(() => cart.filter((cartItem) => cartItem))
        }
    }
};