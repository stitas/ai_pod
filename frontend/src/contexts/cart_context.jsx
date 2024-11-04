import React, { createContext, useState, useEffect } from 'react';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    // Load cart from sessionStorage if available
    const savedCart = sessionStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });
  const [cartSum, setCartSum] = useState(0);

  const addToCart = (cartItem) => {
    console.log(cartItem)
    setCart((prevCart) => {
      const existingItem = prevCart.find((item) => item.id === cartItem.id);
      if (existingItem) {
        return prevCart.map((item) =>
          item.id === cartItem.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      } else {
        return [...prevCart, { ...cartItem, quantity: 1 }];
      }
    });
  };

  const removeFromCart = (cartItem) => {
    setCart((prevCart) => {
      const existingItem = prevCart.find((item) => item.id === cartItem.id);
      if (existingItem.quantity > 1) {
        return prevCart.map((item) =>
          item.id === cartItem.id ? { ...item, quantity: item.quantity - 1 } : item
        );
      } else {
        return prevCart.filter((item) => item.id !== cartItem.id);
      }
    });
  };

  const removeFromCartCompletely = (cartItem) => {
    setCart((prevCart) => {
      return prevCart.filter((item) => item.id !== cartItem.id);
    });
  };

  const clearCart = () => {
    setCart([]);
  };

  const setAllCart = (mockups) => {
    setCart(mockups);
  };

  const getCartSum = () => {
    const sum = cart.reduce((total, item) => total + item.price * item.quantity, 0);
    setCartSum(sum);
  };

  // Save cart to sessionStorage whenever it changes
  useEffect(() => {
    sessionStorage.setItem('cart', JSON.stringify(cart));
    getCartSum();
  }, [cart]);

  return (
    <CartContext.Provider value={{ cart, cartSum, addToCart, removeFromCart, removeFromCartCompletely, clearCart, setAllCart }}>
      {children}
    </CartContext.Provider>
  );
};
