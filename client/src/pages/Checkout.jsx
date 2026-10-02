import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import api from '../api/axios';

const Checkout = () => {
  const { cartItems, subtotal, deliveryFee, grandTotal, clearCart } = useCart();
  const { user } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: user?.name || '',
    phone: '',
    address: '',
    city: '',
    state: '',
    pincode: '',
  });

  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  // If cart is empty, redirect to products
  if (cartItems.length === 0) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 bg-white rounded-3xl border border-gray-100 shadow-sm text-center">
        <h2 className="text-xl font-bold text-gray-900 mb-2">No Items to Checkout</h2>
        <p className="text-sm text-gray-500 mb-6">
          Your cart is currently empty. Add products before proceeding to checkout.
        </p>
        <Link
          to="/products"
          className="px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-semibold hover:bg-indigo-700 transition"
        >
          Browse Products
        </Link>
      </div>
    );
  }

  const validate = () => {
    const newErrors = {};

    if (!formData.fullName.trim()) newErrors.fullName = 'Full Name is required';
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\d{10}$/.test(formData.phone.trim())) {
      newErrors.phone = 'Enter a valid 10-digit mobile number';
    }
    if (!formData.address.trim()) newErrors.address = 'Street address is required';
    if (!formData.city.trim()) newErrors.city = 'City is required';
    if (!formData.state.trim()) newErrors.state = 'State is required';
    if (!formData.pincode.trim()) {
      newErrors.pincode = 'Pincode is required';
    } else if (!/^\d{6}$/.test(formData.pincode.trim())) {
      newErrors.pincode = 'Enter a valid 6-digit postal pincode';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: '' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      showToast('Please fix the form errors before submitting', 'error');
      return;
    }

    try {
      setSubmitting(true);

      const orderPayload = {
        products: cartItems.map((item) => ({
          product: item._id,
          quantity: item.quantity,
          price: item.price,
          name: item.name,
          image: item.image,
        })),
        shippingAddress: {
          fullName: formData.fullName,
          phone: formData.phone,
          address: formData.address,
          city: formData.city,
          state: formData.state,
          pincode: formData.pincode,
        },
        paymentMethod: 'Cash on Delivery',
        totalAmount: grandTotal,
      };

      try {
        // Try live backend API call
        await api.post('/orders', orderPayload);
      } catch (apiErr) {
        // Save to local storage mock orders for demo continuity
        const existingLocalOrders = JSON.parse(localStorage.getItem('ecommerce_mock_orders') || '[]');
        const newMockOrder = {
          _id: 'ORD-' + Math.floor(10000 + Math.random() * 90000),
          createdAt: new Date().toISOString(),
          customerName: formData.fullName,
          customerEmail: user?.email || 'customer@demo.com',
          status: 'Pending',
          paymentMethod: 'Cash on Delivery',
          totalAmount: grandTotal,
          products: orderPayload.products,
          shippingAddress: orderPayload.shippingAddress,
        };
        localStorage.setItem(
          'ecommerce_mock_orders',
          JSON.stringify([newMockOrder, ...existingLocalOrders])
        );
      }

      clearCart();
      showToast('Order placed successfully with Cash on Delivery!', 'success');
      navigate('/my-orders');
    } catch (err) {
      showToast('Failed to place order. Please try again.', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div className="pb-4 border-b border-gray-100">
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Checkout</h1>
        <p className="text-sm text-gray-500 mt-1">
          Complete your delivery details to place your order with Cash on Delivery
        </p>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Delivery Address Form (2 cols) */}
        <div className="lg:col-span-2 bg-white rounded-3xl p-6 sm:p-8 border border-gray-100 shadow-sm space-y-6">
          <div className="flex items-center gap-3 pb-4 border-b border-gray-100">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-sm">
              1
            </div>
            <h2 className="text-lg font-bold text-gray-900">Shipping & Delivery Details</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Full Name */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Full Name *
              </label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="e.g. Vaishnavi Argade"
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.fullName
                    ? 'border-rose-300 focus:ring-rose-200'
                    : 'border-gray-200 focus:ring-indigo-100 focus:border-indigo-600'
                }`}
              />
              {errors.fullName && <p className="text-xs text-rose-500 mt-1">{errors.fullName}</p>}
            </div>

            {/* Phone */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Phone Number (10 digits) *
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="e.g. 9876543210"
                maxLength={10}
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.phone
                    ? 'border-rose-300 focus:ring-rose-200'
                    : 'border-gray-200 focus:ring-indigo-100 focus:border-indigo-600'
                }`}
              />
              {errors.phone && <p className="text-xs text-rose-500 mt-1">{errors.phone}</p>}
            </div>

            {/* Street Address */}
            <div className="sm:col-span-2">
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Flat / House No. / Street Address *
              </label>
              <textarea
                name="address"
                rows={2}
                value={formData.address}
                onChange={handleChange}
                placeholder="e.g. Flat 402, Sunshine Heights, MG Road"
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.address
                    ? 'border-rose-300 focus:ring-rose-200'
                    : 'border-gray-200 focus:ring-indigo-100 focus:border-indigo-600'
                }`}
              />
              {errors.address && <p className="text-xs text-rose-500 mt-1">{errors.address}</p>}
            </div>

            {/* City */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                City *
              </label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="e.g. Pune"
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.city
                    ? 'border-rose-300 focus:ring-rose-200'
                    : 'border-gray-200 focus:ring-indigo-100 focus:border-indigo-600'
                }`}
              />
              {errors.city && <p className="text-xs text-rose-500 mt-1">{errors.city}</p>}
            </div>

            {/* State */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                State *
              </label>
              <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
                placeholder="e.g. Maharashtra"
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.state
                    ? 'border-rose-300 focus:ring-rose-200'
                    : 'border-gray-200 focus:ring-indigo-100 focus:border-indigo-600'
                }`}
              />
              {errors.state && <p className="text-xs text-rose-500 mt-1">{errors.state}</p>}
            </div>

            {/* Pincode */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Pincode (6 digits) *
              </label>
              <input
                type="text"
                name="pincode"
                value={formData.pincode}
                onChange={handleChange}
                placeholder="e.g. 411001"
                maxLength={6}
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.pincode
                    ? 'border-rose-300 focus:ring-rose-200'
                    : 'border-gray-200 focus:ring-indigo-100 focus:border-indigo-600'
                }`}
              />
              {errors.pincode && <p className="text-xs text-rose-500 mt-1">{errors.pincode}</p>}
            </div>
          </div>

          {/* Payment Method Section (Fixed to Cash on Delivery) */}
          <div className="pt-6 border-t border-gray-100">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-sm">
                2
              </div>
              <h2 className="text-lg font-bold text-gray-900">Payment Option</h2>
            </div>

            <div className="p-4 rounded-2xl border-2 border-indigo-600 bg-indigo-50/50 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <input
                  type="radio"
                  id="cod"
                  name="paymentMethod"
                  checked
                  readOnly
                  className="w-4 h-4 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="cod" className="cursor-pointer">
                  <div className="font-semibold text-sm text-gray-900">Cash on Delivery (COD)</div>
                  <div className="text-xs text-gray-500">
                    Pay securely using cash when your package is delivered to your doorstep.
                  </div>
                </label>
              </div>
              <span className="text-xs font-bold text-indigo-700 bg-white px-2.5 py-1 rounded-full border border-indigo-200">
                Recommended
              </span>
            </div>
          </div>
        </div>

        {/* Order Summary & Confirm (1 col) */}
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm space-y-6">
          <h2 className="text-lg font-bold text-gray-900 pb-3 border-b border-gray-100">
            Order Review
          </h2>

          {/* Product Items List in Order */}
          <div className="max-h-60 overflow-y-auto space-y-3 pr-1">
            {cartItems.map((item) => (
              <div key={item._id} className="flex items-center gap-3 text-xs">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-12 h-12 rounded-lg object-cover bg-gray-50 flex-shrink-0"
                />
                <div className="flex-1 truncate">
                  <div className="font-semibold text-gray-900 truncate">{item.name}</div>
                  <div className="text-gray-400">Qty: {item.quantity} × ₹{item.price}</div>
                </div>
                <div className="font-bold text-gray-900">
                  ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                </div>
              </div>
            ))}
          </div>

          <div className="pt-4 border-t border-gray-100 space-y-2 text-sm">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span className="font-semibold text-gray-900">₹{subtotal.toLocaleString('en-IN')}</span>
            </div>
            <div className="flex justify-between text-gray-600">
              <span>Delivery Charges</span>
              <span className="font-semibold text-emerald-600">
                {deliveryFee === 0 ? 'FREE' : `₹${deliveryFee}`}
              </span>
            </div>
            <div className="pt-3 border-t border-gray-100 flex justify-between items-baseline">
              <span className="text-base font-bold text-gray-900">Total Payable</span>
              <span className="text-2xl font-extrabold text-indigo-600">
                ₹{grandTotal.toLocaleString('en-IN')}
              </span>
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-4 px-6 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-2xl shadow-lg shadow-indigo-200 transition transform hover:-translate-y-0.5 text-center flex items-center justify-center gap-2"
          >
            {submitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Placing Order...</span>
              </>
            ) : (
              <span>Place Order (COD)</span>
            )}
          </button>

          <p className="text-[11px] text-gray-400 text-center">
            By placing your order, you agree to our standard demo store conditions.
          </p>
        </div>
      </form>
    </div>
  );
};

export default Checkout;
