import React, { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState(() => {
    try {
      const saved = localStorage.getItem('ecommerce_cart');
      return saved ? JSON.parse(saved) : [];
    } catch (err) {
      console.error('Failed to load cart from localStorage', err);
      return [];
    }
  });

  // Persist to localStorage on change
  useEffect(() => {
    localStorage.setItem('ecommerce_cart', JSON.stringify(cartItems));
  }, [cartItems]);

  // Add item with stock limit validation
  const addToCart = (product, quantity = 1) => {
    if (!product || product.stock <= 0) {
      return { success: false, message: 'This product is out of stock' };
    }

    let addedSuccessfully = true;
    let message = 'Product added to cart';

    setCartItems((prevItems) => {
      const existingIndex = prevItems.findIndex((item) => item._id === product._id);

      if (existingIndex > -1) {
        const existingItem = prevItems[existingIndex];
        const newQty = existingItem.quantity + quantity;

        if (newQty > product.stock) {
          addedSuccessfully = false;
          message = `Cannot add more. Only ${product.stock} in stock.`;
          return prevItems;
        }

        const updated = [...prevItems];
        updated[existingIndex] = { ...existingItem, quantity: newQty };
        return updated;
      } else {
        if (quantity > product.stock) {
          addedSuccessfully = false;
          message = `Cannot add ${quantity}. Only ${product.stock} in stock.`;
          return prevItems;
        }

        return [
          ...prevItems,
          {
            _id: product._id,
            name: product.name,
            price: product.price,
            image: product.image,
            stock: product.stock,
            categoryName: product.categoryName || '',
            quantity,
          },
        ];
      }
    });

    return { success: addedSuccessfully, message };
  };

  // Increase quantity
  const increaseQuantity = (productId) => {
    let allowed = true;
    let maxStock = 0;

    setCartItems((prevItems) =>
      prevItems.map((item) => {
        if (item._id === productId) {
          if (item.quantity + 1 > item.stock) {
            allowed = false;
            maxStock = item.stock;
            return item;
          }
          return { ...item, quantity: item.quantity + 1 };
        }
        return item;
      })
    );

    return {
      success: allowed,
      message: allowed ? 'Quantity updated' : `Maximum stock limit of ${maxStock} reached`,
    };
  };

  // Decrease quantity
  const decreaseQuantity = (productId) => {
    setCartItems((prevItems) =>
      prevItems
        .map((item) => {
          if (item._id === productId) {
            return { ...item, quantity: item.quantity - 1 };
          }
          return item;
        })
        .filter((item) => item.quantity > 0)
    );
  };

  // Remove single product
  const removeFromCart = (productId) => {
    setCartItems((prevItems) => prevItems.filter((item) => item._id !== productId));
  };

  // Clear entire cart
  const clearCart = () => {
    setCartItems([]);
  };

  // Computed totals
  const totalQuantity = cartItems.reduce((acc, item) => acc + item.quantity, 0);
  const subtotal = cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);
  const deliveryFee = subtotal > 0 && subtotal < 1000 ? 99 : 0; // Free delivery over ₹1000
  const grandTotal = subtotal + deliveryFee;

  const value = {
    cartItems,
    addToCart,
    removeFromCart,
    increaseQuantity,
    decreaseQuantity,
    clearCart,
    totalQuantity,
    subtotal,
    deliveryFee,
    grandTotal,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export default CartContext;
