import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useToast } from '../components/Toast';
import { initialProducts } from '../data/mockData';
import api from '../api/axios';

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { showToast } = useToast();

  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        setError(null);
        // Try real API first
        const res = await api.get(`/products/${id}`);
        if (res.data) {
          setProduct(res.data);
          return;
        }
      } catch (err) {
        // Fallback to local mock data
        const found = initialProducts.find((p) => p._id === id);
        if (found) {
          setProduct(found);
        } else {
          setError('Product not found.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium">Loading product details...</p>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 text-center bg-white rounded-3xl border border-gray-100 shadow-sm">
        <h2 className="text-xl font-bold text-gray-900 mb-2">Product Not Found</h2>
        <p className="text-sm text-gray-500 mb-6">
          The product you are looking for may have been removed or does not exist.
        </p>
        <Link
          to="/products"
          className="px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-semibold hover:bg-indigo-700 transition"
        >
          Back to Products
        </Link>
      </div>
    );
  }

  const isOutOfStock = product.stock <= 0;

  const handleQuantityChange = (delta) => {
    const newQty = quantity + delta;
    if (newQty >= 1 && newQty <= product.stock) {
      setQuantity(newQty);
    }
  };

  const handleAddToCart = () => {
    if (isOutOfStock) return;
    const res = addToCart(product, quantity);
    if (res.success) {
      showToast(`Added ${quantity} ${product.name} to cart!`, 'success');
    } else {
      showToast(res.message, 'warning');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Breadcrumb & Back Button */}
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <Link to="/products" className="hover:text-indigo-600 transition flex items-center gap-1">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Products
        </Link>
        <span>/</span>
        <span className="text-gray-900 font-medium truncate">{product.name}</span>
      </div>

      {/* Main Product Showcase Card */}
      <div className="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 sm:p-10 grid grid-cols-1 md:grid-cols-2 gap-10">
        {/* Large Product Image */}
        <div className="aspect-square rounded-2xl overflow-hidden bg-gray-50 border border-gray-100 flex items-center justify-center">
          <img
            src={product.image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800'}
            alt={product.name}
            className="w-full h-full object-cover object-center"
          />
        </div>

        {/* Product Info & Actions */}
        <div className="flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            {/* Category tag & stock badge */}
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full">
                {product.categoryName || 'General Product'}
              </span>
              <span
                className={`text-xs font-bold px-3 py-1 rounded-full ${
                  isOutOfStock
                    ? 'bg-rose-100 text-rose-700'
                    : product.stock <= 5
                    ? 'bg-amber-100 text-amber-700'
                    : 'bg-emerald-100 text-emerald-700'
                }`}
              >
                {isOutOfStock ? 'Out of Stock' : `${product.stock} units available`}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 leading-tight">
              {product.name}
            </h1>

            {/* Price */}
            <div className="flex items-baseline gap-3">
              <span className="text-3xl font-extrabold text-gray-900">
                ₹{Number(product.price).toLocaleString('en-IN')}
              </span>
              <span className="text-xs text-gray-400">Inclusive of all taxes</span>
            </div>

            {/* Description */}
            <div className="pt-4 border-t border-gray-100">
              <h3 className="text-sm font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                {product.description}
              </p>
            </div>
          </div>

          {/* Quantity selector & Add to cart */}
          <div className="space-y-4 pt-6 border-t border-gray-100">
            {!isOutOfStock && (
              <div className="flex items-center gap-4">
                <span className="text-sm font-semibold text-gray-700">Quantity:</span>
                <div className="flex items-center border border-gray-200 rounded-xl overflow-hidden bg-gray-50">
                  <button
                    type="button"
                    onClick={() => handleQuantityChange(-1)}
                    disabled={quantity <= 1}
                    className="px-3 py-1.5 text-gray-600 hover:bg-gray-200 disabled:opacity-40 transition"
                  >
                    -
                  </button>
                  <span className="px-4 py-1.5 text-sm font-bold text-gray-900 bg-white">
                    {quantity}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleQuantityChange(1)}
                    disabled={quantity >= product.stock}
                    className="px-3 py-1.5 text-gray-600 hover:bg-gray-200 disabled:opacity-40 transition"
                  >
                    +
                  </button>
                </div>
                <span className="text-xs text-gray-400">
                  (Max {product.stock})
                </span>
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-3">
              <button
                type="button"
                onClick={handleAddToCart}
                disabled={isOutOfStock}
                className={`flex-1 py-3.5 px-6 rounded-2xl font-bold text-sm transition flex items-center justify-center gap-2 ${
                  isOutOfStock
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-200 hover:-translate-y-0.5'
                }`}
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                {isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
              </button>

              <button
                type="button"
                onClick={() => {
                  if (!isOutOfStock) {
                    addToCart(product, quantity);
                    navigate('/cart');
                  }
                }}
                disabled={isOutOfStock}
                className="py-3.5 px-6 bg-gray-900 hover:bg-black text-white text-sm font-semibold rounded-2xl transition disabled:opacity-50"
              >
                Buy Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
