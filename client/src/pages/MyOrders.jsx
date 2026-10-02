import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { initialOrders } from '../data/mockData';
import api from '../api/axios';

const MyOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        // Try real API first
        const res = await api.get('/orders/my-orders');
        if (res.data && res.data.length > 0) {
          setOrders(res.data);
          return;
        }
      } catch (err) {
        // Fallback to local storage placed orders + initial mock orders
        const localPlaced = JSON.parse(localStorage.getItem('ecommerce_mock_orders') || '[]');
        const combined = [...localPlaced, ...initialOrders];
        setOrders(combined);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Delivered':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Delivered
          </span>
        );
      case 'Shipped':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-800 border border-purple-200">
            <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
            Shipped
          </span>
        );
      case 'Confirmed':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-800 border border-blue-200">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
            Confirmed
          </span>
        );
      case 'Cancelled':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
            Cancelled
          </span>
        );
      case 'Pending':
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-ping"></span>
            Pending
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium">Loading your orders...</p>
      </div>
    );
  }

  if (orders.length === 0) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 bg-white rounded-3xl border border-gray-100 shadow-sm text-center">
        <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">No Orders Yet</h2>
        <p className="text-sm text-gray-500 mb-6">
          You haven't placed any orders yet. Once you place an order, you can track it here!
        </p>
        <Link
          to="/products"
          className="px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-semibold hover:bg-indigo-700 transition"
        >
          Start Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div className="pb-4 border-b border-gray-100">
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">My Orders</h1>
        <p className="text-sm text-gray-500 mt-1">
          Review your previous purchases and real-time delivery status
        </p>
      </div>

      {/* Orders List */}
      <div className="space-y-6">
        {orders.map((order) => (
          <div
            key={order._id}
            className="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden transition hover:shadow-sm"
          >
            {/* Order Card Header */}
            <div className="bg-gray-50/80 px-6 py-4 border-b border-gray-100 flex flex-wrap items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-6 text-xs text-gray-500">
                <div>
                  <span className="block font-medium">Order Placed</span>
                  <span className="font-semibold text-gray-900">
                    {new Date(order.createdAt).toLocaleDateString('en-IN', {
                      day: 'numeric',
                      month: 'short',
                      year: 'numeric',
                    })}
                  </span>
                </div>
                <div>
                  <span className="block font-medium">Order ID</span>
                  <span className="font-mono font-semibold text-gray-900">{order._id}</span>
                </div>
                <div>
                  <span className="block font-medium">Payment</span>
                  <span className="font-semibold text-gray-900">{order.paymentMethod || 'Cash on Delivery'}</span>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <span className="block text-xs text-gray-500 font-medium">Total Amount</span>
                  <span className="text-base font-extrabold text-indigo-600">
                    ₹{Number(order.totalAmount).toLocaleString('en-IN')}
                  </span>
                </div>
                <div>{getStatusBadge(order.status)}</div>
              </div>
            </div>

            {/* Order Products & Details */}
            <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Product items (2 cols) */}
              <div className="md:col-span-2 space-y-4">
                <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                  Ordered Items
                </h4>
                <div className="divide-y divide-gray-100">
                  {order.products?.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-4 py-3 first:pt-0 last:pb-0">
                      <img
                        src={item.image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'}
                        alt={item.name}
                        className="w-14 h-14 rounded-xl object-cover bg-gray-50 border border-gray-100 flex-shrink-0"
                      />
                      <div className="flex-1 min-w-0">
                        <h5 className="text-sm font-semibold text-gray-900 truncate">
                          {item.name}
                        </h5>
                        <p className="text-xs text-gray-500">
                          Qty: {item.quantity} × ₹{Number(item.price).toLocaleString('en-IN')}
                        </p>
                      </div>
                      <div className="text-sm font-bold text-gray-900">
                        ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Delivery Address (1 col) */}
              <div className="bg-gray-50/50 p-4 rounded-2xl border border-gray-100 space-y-2 text-xs">
                <h4 className="font-semibold text-gray-400 uppercase tracking-wider">
                  Shipping Address
                </h4>
                <p className="font-bold text-gray-900 text-sm">
                  {order.shippingAddress?.fullName}
                </p>
                <p className="text-gray-600 leading-relaxed">
                  {order.shippingAddress?.address}
                  <br />
                  {order.shippingAddress?.city}, {order.shippingAddress?.state} -{' '}
                  {order.shippingAddress?.pincode}
                </p>
                <p className="text-gray-500 pt-1">
                  📞 Phone: <span className="font-medium text-gray-900">{order.shippingAddress?.phone}</span>
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyOrders;
