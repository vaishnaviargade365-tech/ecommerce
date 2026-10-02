import React, { useState, useEffect } from 'react';
import AdminLayout from './AdminLayout';
import { useToast } from '../../components/Toast';
import { initialOrders } from '../../data/mockData';
import api from '../../api/axios';

const ManageOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrderDetails, setSelectedOrderDetails] = useState(null);
  const { showToast } = useToast();

  const statusOptions = ['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled'];

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        const res = await api.get('/admin/orders');
        if (res.data && res.data.length > 0) {
          setOrders(res.data);
          return;
        }
      } catch (err) {
        // Fallback to local placed orders + mock orders
        const localPlaced = JSON.parse(localStorage.getItem('ecommerce_mock_orders') || '[]');
        setOrders([...localPlaced, ...initialOrders]);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const handleStatusChange = async (orderId, newStatus) => {
    try {
      try {
        // Try real API endpoint: PATCH /api/admin/orders/:id/status
        await api.patch(`/admin/orders/${orderId}/status`, { status: newStatus });
      } catch (apiErr) {
        // Local fallback
      }

      const updated = orders.map((o) => (o._id === orderId ? { ...o, status: newStatus } : o));
      setOrders(updated);

      // Update in local mock storage if present
      const localPlaced = JSON.parse(localStorage.getItem('ecommerce_mock_orders') || '[]');
      const updatedLocal = localPlaced.map((o) =>
        o._id === orderId ? { ...o, status: newStatus } : o
      );
      localStorage.setItem('ecommerce_mock_orders', JSON.stringify(updatedLocal));

      showToast(`Order ${orderId} marked as ${newStatus}`, 'success');
    } catch (err) {
      showToast('Failed to update status', 'error');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Delivered':
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'Shipped':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'Confirmed':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'Cancelled':
        return 'bg-rose-100 text-rose-800 border-rose-200';
      case 'Pending':
      default:
        return 'bg-amber-100 text-amber-800 border-amber-200';
    }
  };

  return (
    <AdminLayout title="Manage Customer Orders">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-gray-100">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
              Manage Orders
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Review customer delivery manifests and update order fulfillment lifecycle ({orders.length} orders)
            </p>
          </div>
        </div>

        {/* Orders Table */}
        <div className="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs sm:text-sm">
              <thead className="bg-gray-50/70 text-gray-400 uppercase text-[11px] tracking-wider">
                <tr>
                  <th className="py-3.5 px-6">Order ID</th>
                  <th className="py-3.5 px-6">Customer</th>
                  <th className="py-3.5 px-6">Date</th>
                  <th className="py-3.5 px-6">Total Amount</th>
                  <th className="py-3.5 px-6">Current Status</th>
                  <th className="py-3.5 px-6">Update Status</th>
                  <th className="py-3.5 px-6 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 font-medium">
                {orders.map((ord) => (
                  <tr key={ord._id} className="hover:bg-gray-50/60 transition">
                    <td className="py-4 px-6 font-mono font-bold text-gray-900">{ord._id}</td>
                    <td className="py-4 px-6">
                      <div className="font-semibold text-gray-900">{ord.customerName}</div>
                      <div className="text-[11px] text-gray-400">{ord.shippingAddress?.phone}</div>
                    </td>
                    <td className="py-4 px-6 text-gray-500">
                      {new Date(ord.createdAt).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                      })}
                    </td>
                    <td className="py-4 px-6 font-bold text-gray-900">
                      ₹{Number(ord.totalAmount).toLocaleString('en-IN')}
                    </td>
                    <td className="py-4 px-6">
                      <span
                        className={`inline-block px-2.5 py-1 rounded-full text-xs font-bold border ${getStatusColor(
                          ord.status
                        )}`}
                      >
                        {ord.status}
                      </span>
                    </td>
                    {/* Status updater dropdown */}
                    <td className="py-4 px-6">
                      <select
                        value={ord.status}
                        onChange={(e) => handleStatusChange(ord._id, e.target.value)}
                        className="px-3 py-1.5 rounded-xl border border-gray-200 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 bg-white transition cursor-pointer"
                      >
                        {statusOptions.map((st) => (
                          <option key={st} value={st}>
                            {st}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={() => setSelectedOrderDetails(ord)}
                        className="px-3 py-1.5 bg-gray-100 hover:bg-indigo-50 text-gray-700 hover:text-indigo-600 rounded-lg text-xs font-semibold transition"
                      >
                        View Items
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Order Details Modal */}
        {selectedOrderDetails && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-gray-100 max-h-[90vh] overflow-y-auto space-y-6 animate-scale-up">
              <div className="flex items-center justify-between pb-3 border-b border-gray-100">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">
                    Order {selectedOrderDetails._id}
                  </h3>
                  <span className="text-xs text-gray-400">
                    Placed on {new Date(selectedOrderDetails.createdAt).toLocaleString('en-IN')}
                  </span>
                </div>
                <button
                  onClick={() => setSelectedOrderDetails(null)}
                  className="p-2 text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              {/* Delivery info */}
              <div className="p-4 bg-gray-50 rounded-2xl text-xs space-y-1">
                <span className="font-semibold text-gray-400 uppercase tracking-wider block mb-1">
                  Recipient Details
                </span>
                <p className="font-bold text-gray-900 text-sm">
                  {selectedOrderDetails.shippingAddress?.fullName}
                </p>
                <p className="text-gray-600">
                  {selectedOrderDetails.shippingAddress?.address},{' '}
                  {selectedOrderDetails.shippingAddress?.city},{' '}
                  {selectedOrderDetails.shippingAddress?.state} -{' '}
                  {selectedOrderDetails.shippingAddress?.pincode}
                </p>
                <p className="text-gray-500 pt-1">
                  📞 {selectedOrderDetails.shippingAddress?.phone}
                </p>
              </div>

              {/* Items */}
              <div className="space-y-3">
                <span className="font-semibold text-gray-400 uppercase tracking-wider text-xs block">
                  Ordered Products
                </span>
                <div className="divide-y divide-gray-100">
                  {selectedOrderDetails.products?.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-3 py-2 text-xs">
                      <img
                        src={item.image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'}
                        alt={item.name}
                        className="w-12 h-12 rounded-lg object-cover bg-gray-50 border border-gray-100 flex-shrink-0"
                      />
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-gray-900 truncate">{item.name}</p>
                        <p className="text-gray-400">Qty: {item.quantity} × ₹{item.price}</p>
                      </div>
                      <span className="font-bold text-gray-900">
                        ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                <span className="text-sm font-bold text-gray-900">Total Amount:</span>
                <span className="text-xl font-extrabold text-indigo-600">
                  ₹{Number(selectedOrderDetails.totalAmount).toLocaleString('en-IN')}
                </span>
              </div>

              <div className="text-right">
                <button
                  type="button"
                  onClick={() => setSelectedOrderDetails(null)}
                  className="px-5 py-2 text-sm font-semibold bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl transition"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

export default ManageOrders;
