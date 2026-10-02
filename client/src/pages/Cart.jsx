import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useToast } from '../components/Toast';

const Cart = () => {
  const {
    cartItems,
    increaseQuantity,
    decreaseQuantity,
    removeFromCart,
    clearCart,
    subtotal,
    deliveryFee,
    grandTotal,
    totalQuantity,
  } = useCart();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const handleIncrease = (id) => {
    const res = increaseQuantity(id);
    if (!res.success) {
      showToast(res.message, 'warning');
    }
  };

  const handleRemove = (id, name) => {
    removeFromCart(id);
    showToast(`${name} removed from cart`, 'info');
  };

  // 1. Empty Cart UI
  if (cartItems.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-md mx-auto bg-white rounded-3xl p-10 text-center border border-gray-100 shadow-sm">
          <div className="w-20 h-20 bg-indigo-50 text-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.6} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Your cart is empty</h2>
          <p className="text-gray-500 text-sm mb-8 leading-relaxed">
            Looks like you haven't added anything to your cart yet. Explore our featured products and discover great deals.
          </p>
          <Link
            to="/products"
            className="inline-flex items-center justify-center gap-2 w-full py-3.5 px-6 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-2xl shadow-lg shadow-indigo-200 transition"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  // 2. Active Cart UI
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between pb-6 border-b border-gray-100">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Shopping Cart</h1>
          <p className="text-sm text-gray-500 mt-1">
            You have {totalQuantity} {totalQuantity === 1 ? 'item' : 'items'} in your cart
          </p>
        </div>
        <button
          onClick={clearCart}
          className="text-xs font-semibold text-rose-600 hover:text-rose-700 hover:bg-rose-50 px-3 py-1.5 rounded-lg transition"
        >
          Clear Cart
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Cart Items List (2 cols on large screen) */}
        <div className="lg:col-span-2 space-y-4">
          {cartItems.map((item) => (
            <div
              key={item._id}
              className="bg-white rounded-2xl p-4 sm:p-5 border border-gray-100 shadow-xs flex flex-col sm:flex-row items-center gap-4 sm:gap-6"
            >
              {/* Product Image */}
              <Link
                to={`/products/${item._id}`}
                className="w-24 h-24 sm:w-28 sm:h-28 rounded-xl overflow-hidden bg-gray-50 flex-shrink-0 border border-gray-100"
              >
                <img
                  src={item.image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'}
                  alt={item.name}
                  className="w-full h-full object-cover object-center"
                />
              </Link>

              {/* Title & Price Details */}
              <div className="flex-1 w-full space-y-1 text-center sm:text-left">
                <Link
                  to={`/products/${item._id}`}
                  className="font-semibold text-gray-900 text-sm sm:text-base hover:text-indigo-600 transition"
                >
                  {item.name}
                </Link>
                <div className="text-xs text-gray-400">
                  Unit Price: ₹{Number(item.price).toLocaleString('en-IN')}
                </div>
                <div className="text-xs font-medium text-emerald-600">
                  {item.stock} available in stock
                </div>
              </div>

              {/* Quantity Controls */}
              <div className="flex items-center gap-3">
                <div className="flex items-center border border-gray-200 rounded-xl overflow-hidden bg-gray-50">
                  <button
                    onClick={() => decreaseQuantity(item._id)}
                    className="px-2.5 py-1 text-gray-600 hover:bg-gray-200 transition"
                    aria-label="Decrease quantity"
                  >
                    -
                  </button>
                  <span className="px-3 py-1 text-xs font-bold text-gray-900 bg-white">
                    {item.quantity}
                  </span>
                  <button
                    onClick={() => handleIncrease(item._id)}
                    className="px-2.5 py-1 text-gray-600 hover:bg-gray-200 transition"
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>

                {/* Subtotal for Item */}
                <div className="text-right min-w-[80px]">
                  <div className="text-sm font-bold text-gray-900">
                    ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                  </div>
                </div>

                {/* Remove button */}
                <button
                  onClick={() => handleRemove(item._id, item.name)}
                  className="p-2 text-gray-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                  aria-label="Remove item"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary Card (1 col on large screen) */}
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm space-y-6">
          <h2 className="text-lg font-bold text-gray-900 pb-3 border-b border-gray-100">
            Order Summary
          </h2>

          <div className="space-y-3 text-sm">
            <div className="flex justify-between text-gray-600">
              <span>Items Total ({totalQuantity})</span>
              <span className="font-semibold text-gray-900">
                ₹{subtotal.toLocaleString('en-IN')}
              </span>
            </div>

            <div className="flex justify-between text-gray-600">
              <span>Delivery Fee</span>
              <span className={`font-semibold ${deliveryFee === 0 ? 'text-emerald-600' : 'text-gray-900'}`}>
                {deliveryFee === 0 ? 'FREE' : `₹${deliveryFee}`}
              </span>
            </div>

            {deliveryFee === 0 && (
              <p className="text-[11px] text-emerald-600 bg-emerald-50 p-2 rounded-xl">
                🎉 Congratulations! You qualify for Free Delivery.
              </p>
            )}

            <div className="pt-3 border-t border-gray-100 flex justify-between items-baseline">
              <span className="text-base font-bold text-gray-900">Grand Total</span>
              <span className="text-2xl font-extrabold text-indigo-600">
                ₹{grandTotal.toLocaleString('en-IN')}
              </span>
            </div>
          </div>

          <button
            onClick={() => navigate('/checkout')}
            className="w-full py-4 px-6 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-2xl shadow-lg shadow-indigo-200 transition transform hover:-translate-y-0.5 text-center flex items-center justify-center gap-2"
          >
            <span>Proceed to Checkout</span>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>

          <Link
            to="/products"
            className="block text-center text-xs font-semibold text-gray-500 hover:text-indigo-600 transition"
          >
            ← Or continue shopping
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Cart;
