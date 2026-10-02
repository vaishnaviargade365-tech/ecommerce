import React, { useState, useEffect } from 'react';
import AdminLayout from './AdminLayout';
import Modal from '../../components/Modal';
import { useToast } from '../../components/Toast';
import { initialProducts, initialCategories } from '../../data/mockData';
import api from '../../api/axios';

const ManageProducts = () => {
  const [products, setProducts] = useState(initialProducts);
  const [categories, setCategories] = useState(initialCategories);
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();

  // Form Modal State
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    image: '',
    category: '',
    stock: '',
  });

  // Delete Modal State
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [productToDelete, setProductToDelete] = useState(null);

  useEffect(() => {
    const fetchCatalog = async () => {
      try {
        setLoading(true);
        const [prodRes, catRes] = await Promise.all([
          api.get('/products'),
          api.get('/categories'),
        ]);
        if (prodRes.data && prodRes.data.length > 0) setProducts(prodRes.data);
        if (catRes.data && catRes.data.length > 0) setCategories(catRes.data);
      } catch (err) {
        // Fallback to local storage if present
        const savedProds = localStorage.getItem('ecommerce_mock_products');
        if (savedProds) setProducts(JSON.parse(savedProds));
      } finally {
        setLoading(false);
      }
    };
    fetchCatalog();
  }, []);

  const saveProductsLocal = (newProds) => {
    setProducts(newProds);
    localStorage.setItem('ecommerce_mock_products', JSON.stringify(newProds));
  };

  const handleOpenAdd = () => {
    setEditingProduct(null);
    setFormData({
      name: '',
      description: '',
      price: '',
      image: '',
      category: categories[0]?._id || '',
      stock: '',
    });
    setIsFormOpen(true);
  };

  const handleOpenEdit = (p) => {
    setEditingProduct(p);
    setFormData({
      name: p.name,
      description: p.description || '',
      price: p.price,
      image: p.image || '',
      category: p.category || categories[0]?._id || '',
      stock: p.stock,
    });
    setIsFormOpen(true);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.price || formData.stock === '') {
      showToast('Name, price, and stock are required', 'error');
      return;
    }

    const selectedCat = categories.find((c) => c._id === formData.category);
    const categoryName = selectedCat ? selectedCat.name : 'General';

    const payload = {
      name: formData.name.trim(),
      description: formData.description.trim(),
      price: Number(formData.price),
      image: formData.image.trim() || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500',
      category: formData.category,
      categoryName,
      stock: Number(formData.stock),
    };

    try {
      if (editingProduct) {
        try {
          await api.put(`/products/${editingProduct._id}`, payload);
        } catch (apiErr) {
          // Local fallback
        }
        const updated = products.map((item) =>
          item._id === editingProduct._id ? { ...item, ...payload } : item
        );
        saveProductsLocal(updated);
        showToast('Product updated successfully!', 'success');
      } else {
        const newProduct = {
          _id: 'prod_' + Date.now(),
          ...payload,
        };
        try {
          await api.post('/products', payload);
        } catch (apiErr) {
          // Local fallback
        }
        saveProductsLocal([newProduct, ...products]);
        showToast('Product created successfully!', 'success');
      }
      setIsFormOpen(false);
    } catch (err) {
      showToast('Error saving product', 'error');
    }
  };

  const handleConfirmDelete = async () => {
    if (!productToDelete) return;
    try {
      try {
        await api.delete(`/products/${productToDelete._id}`);
      } catch (apiErr) {
        // Local fallback
      }
      const updated = products.filter((p) => p._id !== productToDelete._id);
      saveProductsLocal(updated);
      showToast(`Product "${productToDelete.name}" deleted.`, 'info');
    } catch (err) {
      showToast('Failed to delete product', 'error');
    } finally {
      setDeleteModalOpen(false);
      setProductToDelete(null);
    }
  };

  return (
    <AdminLayout title="Manage Products">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-gray-100">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
              Manage Products
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Add, update, or remove items from the active store inventory ({products.length} items)
            </p>
          </div>
          <button
            onClick={handleOpenAdd}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-2xl shadow-sm text-xs sm:text-sm flex items-center justify-center gap-2 transition"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add New Product
          </button>
        </div>

        {/* Product Table */}
        <div className="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs sm:text-sm">
              <thead className="bg-gray-50/70 text-gray-400 uppercase text-[11px] tracking-wider">
                <tr>
                  <th className="py-3.5 px-6">Product</th>
                  <th className="py-3.5 px-6">Category</th>
                  <th className="py-3.5 px-6">Price</th>
                  <th className="py-3.5 px-6">Stock Status</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 font-medium">
                {products.map((item) => (
                  <tr key={item._id} className="hover:bg-gray-50/60 transition">
                    {/* Image & Name */}
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <img
                          src={item.image}
                          alt={item.name}
                          className="w-12 h-12 rounded-xl object-cover bg-gray-50 border border-gray-100 flex-shrink-0"
                        />
                        <div className="min-w-0 max-w-xs truncate">
                          <p className="font-semibold text-gray-900 truncate">{item.name}</p>
                          <p className="text-[11px] text-gray-400 truncate">{item.description}</p>
                        </div>
                      </div>
                    </td>

                    {/* Category */}
                    <td className="py-4 px-6">
                      <span className="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs font-semibold rounded-lg">
                        {item.categoryName || 'General'}
                      </span>
                    </td>

                    {/* Price */}
                    <td className="py-4 px-6 font-bold text-gray-900">
                      ₹{Number(item.price).toLocaleString('en-IN')}
                    </td>

                    {/* Stock */}
                    <td className="py-4 px-6">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          item.stock <= 0
                            ? 'bg-rose-100 text-rose-800'
                            : item.stock <= 5
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}
                      >
                        {item.stock <= 0 ? 'Out of stock' : `${item.stock} in stock`}
                      </span>
                    </td>

                    {/* Actions */}
                    <td className="py-4 px-6 text-right space-x-2">
                      <button
                        onClick={() => handleOpenEdit(item)}
                        className="px-3 py-1.5 bg-gray-100 hover:bg-indigo-50 text-gray-700 hover:text-indigo-600 rounded-lg text-xs font-semibold transition"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => {
                          setProductToDelete(item);
                          setDeleteModalOpen(true);
                        }}
                        className="px-3 py-1.5 bg-gray-100 hover:bg-rose-50 text-gray-700 hover:text-rose-600 rounded-lg text-xs font-semibold transition"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Add/Edit Product Modal */}
        {isFormOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-gray-100 max-h-[90vh] overflow-y-auto animate-scale-up">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                {editingProduct ? 'Edit Product Details' : 'Add New Product to Store'}
              </h3>
              <form onSubmit={handleFormSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Product Title *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="e.g. Wireless Noise-Canceling Headphones"
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">
                      Price (₹) *
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={formData.price}
                      onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                      placeholder="e.g. 2499"
                      className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">
                      Available Stock *
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={formData.stock}
                      onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                      placeholder="e.g. 15"
                      className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Category *
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition bg-white"
                  >
                    {categories.map((c) => (
                      <option key={c._id} value={c._id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Product Image URL
                  </label>
                  <input
                    type="url"
                    value={formData.image}
                    onChange={(e) => setFormData({ ...formData, image: e.target.value })}
                    placeholder="https://images.unsplash.com/..."
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                  />
                  <span className="text-[11px] text-gray-400">Leave blank to use a default placeholder</span>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    rows={3}
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Features, materials, battery specifications..."
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
                  <button
                    type="button"
                    onClick={() => setIsFormOpen(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-xl transition"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-xs transition"
                  >
                    {editingProduct ? 'Save Changes' : 'Create Product'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Delete Confirmation Modal */}
        <Modal
          isOpen={deleteModalOpen}
          title="Delete Product"
          message={`Are you sure you want to delete "${productToDelete?.name}"? This product will no longer appear on the public storefront.`}
          confirmText="Yes, Delete Product"
          confirmVariant="danger"
          onConfirm={handleConfirmDelete}
          onCancel={() => {
            setDeleteModalOpen(false);
            setProductToDelete(null);
          }}
        />
      </div>
    </AdminLayout>
  );
};

export default ManageProducts;
