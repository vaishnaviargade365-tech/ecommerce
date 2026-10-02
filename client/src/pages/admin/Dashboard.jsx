import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import AdminLayout from './AdminLayout';
import { initialProducts, initialCategories, initialOrders } from '../../data/mockData';
import api from '../../api/axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalProducts: initialProducts.length,
    totalCategories: initialCategories.length,
    totalOrders: initialOrders.length,
    pendingOrders: initialOrders.filter((o) => o.status === 'Pending').length,
  });

  const [recentOrders, setRecentOrders] = useState(initialOrders);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // Try real API endpoints
        const [prodRes, catRes, orderRes] = await Promise.all([
          api.get('/products'),
          api.get('/categories'),
          api.get('/admin/orders'),
        ]);

        const prods = prodRes.data || [];
        const cats = catRes.data || [];
        const orders = orderRes.data || [];

        setStats({
          totalProducts: prods.length,
          totalCategories: cats.length,
          totalOrders: orders.length,
          pendingOrders: orders.filter((o) => o.status === 'Pending').length,
        });
        setRecentOrders(orders.slice(0, 5));
      } catch (err) {
        // Fallback to local storage placed orders + initial mock orders
        const localPlaced = JSON.parse(localStorage.getItem('ecommerce_mock_orders') || '[]');
        const allOrders = [...localPlaced, ...initialOrders];

        setStats({
          totalProducts: initialProducts.length,
          totalCategories: initialCategories.length,
          totalOrders: allOrders.length,
          pendingOrders: allOrders.filter((o) => o.status === 'Pending').length,
        });
        setRecentOrders(allOrders.slice(0, 5));
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <AdminLayout title="Admin Dashboard">
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
              Dashboard Overview
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Store analytics, inventory summary, and pending order actions
            </p>
          </div>

          {/* Quick Action Links */}
          <div className="flex items-center gap-2">
            <Link
              to="/admin/products"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-xl shadow-xs transition"
            >
              + Add Product
            </Link>
            <Link
              to="/admin/categories"
              className="px-4 py-2 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 text-xs font-semibold rounded-xl shadow-xs transition"
            >
              + Add Category
            </Link>
          </div>
        </div>

        {/* 4 Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {/* Total Products */}
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center flex-shrink-0">
              <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Total Products
              </span>
              <div className="text-2xl font-black text-gray-900 mt-0.5">
                {stats.totalProducts}
              </div>
            </div>
          </div>

          {/* Total Categories */}
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center flex-shrink-0">
              <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Categories
              </span>
              <div className="text-2xl font-black text-gray-900 mt-0.5">
                {stats.totalCategories}
              </div>
            </div>
          </div>

          {/* Total Orders */}
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center flex-shrink-0">
              <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Total Orders
              </span>
              <div className="text-2xl font-black text-gray-900 mt-0.5">
                {stats.totalOrders}
              </div>
            </div>
          </div>

          {/* Pending Orders */}
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center flex-shrink-0">
              <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Pending Orders
              </span>
              <div className="text-2xl font-black text-amber-600 mt-0.5">
                {stats.pendingOrders}
              </div>
            </div>
          </div>
        </div>

        {/* Recent Orders Table */}
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <div>
              <h2 className="text-lg font-bold text-gray-900">Recent Customer Orders</h2>
              <p className="text-xs text-gray-400">Latest customer checkout transactions</p>
            </div>
            <Link
              to="/admin/orders"
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 transition"
            >
              View all orders →
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-gray-400 bg-gray-50/70 uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4 rounded-l-xl">Order ID</th>
                  <th className="py-3 px-4">Customer</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Total</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 rounded-r-xl text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50 font-medium">
                {recentOrders.map((ord) => (
                  <tr key={ord._id} className="hover:bg-gray-50/60 transition">
                    <td className="py-3.5 px-4 font-mono font-bold text-gray-900">{ord._id}</td>
                    <td className="py-3.5 px-4 text-gray-700">{ord.customerName}</td>
                    <td className="py-3.5 px-4 text-gray-500">
                      {new Date(ord.createdAt).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                      })}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-gray-900">
                      ₹{Number(ord.totalAmount).toLocaleString('en-IN')}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-block px-2.5 py-1 rounded-full text-[11px] font-bold ${
                          ord.status === 'Delivered'
                            ? 'bg-emerald-100 text-emerald-800'
                            : ord.status === 'Shipped'
                            ? 'bg-purple-100 text-purple-800'
                            : ord.status === 'Cancelled'
                            ? 'bg-rose-100 text-rose-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}
                      >
                        {ord.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        to="/admin/orders"
                        className="text-indigo-600 hover:text-indigo-800 font-semibold"
                      >
                        Manage
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default Dashboard;
