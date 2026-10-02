import React, { useState, useEffect } from 'react';
import AdminLayout from './AdminLayout';
import Modal from '../../components/Modal';
import { useToast } from '../../components/Toast';
import { initialCategories } from '../../data/mockData';
import api from '../../api/axios';

const ManageCategories = () => {
  const [categories, setCategories] = useState(initialCategories);
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();

  // Modal State
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [formData, setFormData] = useState({ name: '', description: '' });

  // Delete Confirmation State
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [categoryToDelete, setCategoryToDelete] = useState(null);

  useEffect(() => {
    const fetchCats = async () => {
      try {
        setLoading(true);
        const res = await api.get('/categories');
        if (res.data && res.data.length > 0) setCategories(res.data);
      } catch (err) {
        // Fallback to local storage or mock
        const saved = localStorage.getItem('ecommerce_mock_categories');
        if (saved) setCategories(JSON.parse(saved));
      } finally {
        setLoading(false);
      }
    };
    fetchCats();
  }, []);

  const saveToLocal = (newCats) => {
    setCategories(newCats);
    localStorage.setItem('ecommerce_mock_categories', JSON.stringify(newCats));
  };

  const handleOpenAdd = () => {
    setEditingCategory(null);
    setFormData({ name: '', description: '' });
    setIsFormOpen(true);
  };

  const handleOpenEdit = (cat) => {
    setEditingCategory(cat);
    setFormData({ name: cat.name, description: cat.description || '' });
    setIsFormOpen(true);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) {
      showToast('Category name is required', 'error');
      return;
    }

    try {
      if (editingCategory) {
        // Edit existing
        try {
          await api.put(`/categories/${editingCategory._id}`, formData);
        } catch (apiErr) {
          // Local fallback
        }
        const updated = categories.map((c) =>
          c._id === editingCategory._id ? { ...c, ...formData } : c
        );
        saveToLocal(updated);
        showToast('Category updated successfully!', 'success');
      } else {
        // Add new
        const newCat = {
          _id: 'cat_' + Date.now(),
          name: formData.name.trim(),
          description: formData.description.trim(),
        };
        try {
          await api.post('/categories', formData);
        } catch (apiErr) {
          // Local fallback
        }
        saveToLocal([...categories, newCat]);
        showToast('Category added successfully!', 'success');
      }
      setIsFormOpen(false);
    } catch (err) {
      showToast('Failed to save category', 'error');
    }
  };

  const handleConfirmDelete = async () => {
    if (!categoryToDelete) return;
    try {
      try {
        await api.delete(`/categories/${categoryToDelete._id}`);
      } catch (apiErr) {
        // Local fallback
      }
      const updated = categories.filter((c) => c._id !== categoryToDelete._id);
      saveToLocal(updated);
      showToast(`Category "${categoryToDelete.name}" deleted.`, 'info');
    } catch (err) {
      showToast('Failed to delete category', 'error');
    } finally {
      setDeleteModalOpen(false);
      setCategoryToDelete(null);
    }
  };

  return (
    <AdminLayout title="Manage Categories">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-gray-100">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
              Manage Categories
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Add, edit, or remove store classification departments ({categories.length} total)
            </p>
          </div>
          <button
            onClick={handleOpenAdd}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-2xl shadow-sm text-xs sm:text-sm flex items-center justify-center gap-2 transition"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add New Category
          </button>
        </div>

        {/* Categories Table */}
        <div className="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs sm:text-sm">
              <thead className="bg-gray-50/70 text-gray-400 uppercase text-[11px] tracking-wider">
                <tr>
                  <th className="py-3.5 px-6">Category Name</th>
                  <th className="py-3.5 px-6">Description</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 font-medium">
                {categories.map((cat) => (
                  <tr key={cat._id} className="hover:bg-gray-50/60 transition">
                    <td className="py-4 px-6 text-gray-900 font-semibold">{cat.name}</td>
                    <td className="py-4 px-6 text-gray-500 max-w-xs truncate">{cat.description || '—'}</td>
                    <td className="py-4 px-6 text-right space-x-2">
                      <button
                        onClick={() => handleOpenEdit(cat)}
                        className="px-3 py-1.5 bg-gray-100 hover:bg-indigo-50 text-gray-700 hover:text-indigo-600 rounded-lg text-xs font-semibold transition"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => {
                          setCategoryToDelete(cat);
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

        {/* Add/Edit Category Modal */}
        {isFormOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-gray-100 animate-scale-up">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                {editingCategory ? 'Edit Category' : 'Create New Category'}
              </h3>
              <form onSubmit={handleFormSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Category Name *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="e.g. Footwear, Electronics"
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    rows={3}
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Short description of products in this category..."
                    className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
                  />
                </div>
                <div className="flex items-center justify-end gap-3 pt-3">
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
                    {editingCategory ? 'Update' : 'Create'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Delete Confirmation Modal */}
        <Modal
          isOpen={deleteModalOpen}
          title="Delete Category"
          message={`Are you sure you want to delete "${categoryToDelete?.name}"? Any products assigned to this category may become uncategorized.`}
          confirmText="Yes, Delete"
          confirmVariant="danger"
          onConfirm={handleConfirmDelete}
          onCancel={() => {
            setDeleteModalOpen(false);
            setCategoryToDelete(null);
          }}
        />
      </div>
    </AdminLayout>
  );
};

export default ManageCategories;
