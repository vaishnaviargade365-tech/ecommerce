import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useToast } from './Toast';

const ProductCard = ({ product }) => {
  const { addToCart } = useCart();
  const { showToast } = useToast();

  if (!product) return null;

  const isOutOfStock = product.stock <= 0;
  const isLowStock = product.stock > 0 && product.stock <= 5;

  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (isOutOfStock) return;

    const result = addToCart(product, 1);
    if (result.success) {
      showToast(`${product.name} added to cart!`, 'success');
    } else {
      showToast(result.message, 'warning');
    }
  };

  return (
    <div className="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col overflow-hidden h-full">
      {/* Product Image & Badges */}
      <Link to={`/products/${product._id}`} className="relative block aspect-square overflow-hidden bg-gray-50">
        <img
          src={product.image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'}
          alt={product.name}
          className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />

        {/* Category Pill */}
        {product.categoryName && (
          <span className="absolute top-3 left-3 bg-white/90 backdrop-blur-xs text-gray-700 text-[11px] font-semibold px-2.5 py-1 rounded-full shadow-xs">
            {product.categoryName}
          </span>
        )}

        {/* Stock Badge */}
        {isOutOfStock ? (
          <span className="absolute top-3 right-3 bg-rose-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-full shadow-xs">
            Out of Stock
          </span>
        ) : isLowStock ? (
          <span className="absolute top-3 right-3 bg-amber-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-full shadow-xs">
            Only {product.stock} left
          </span>
        ) : null}
      </Link>

      {/* Card Content */}
      <div className="p-4 flex flex-col flex-1">
        <Link to={`/products/${product._id}`} className="group-hover:text-indigo-600 transition-colors">
          <h3 className="font-semibold text-gray-900 text-sm line-clamp-1 mb-1">
            {product.name}
          </h3>
        </Link>

        <p className="text-xs text-gray-500 line-clamp-2 mb-3 flex-1 leading-relaxed">
          {product.description}
        </p>

        {/* Price & Stock info */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-50 mb-3">
          <div>
            <span className="text-xs text-gray-400 font-medium">Price</span>
            <div className="text-base font-bold text-gray-900">
              ₹{Number(product.price).toLocaleString('en-IN')}
            </div>
          </div>
          <div className="text-right">
            <span className="text-xs text-gray-400 font-medium">Availability</span>
            <div className={`text-xs font-semibold ${isOutOfStock ? 'text-rose-600' : 'text-emerald-600'}`}>
              {isOutOfStock ? 'Out of Stock' : `${product.stock} in stock`}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-2 mt-auto">
          <Link
            to={`/products/${product._id}`}
            className="w-full py-2 px-3 text-center text-xs font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl transition"
          >
            Details
          </Link>
          <button
            type="button"
            disabled={isOutOfStock}
            onClick={handleAddToCart}
            className={`w-full py-2 px-3 text-center text-xs font-semibold rounded-xl transition flex items-center justify-center gap-1.5 ${
              isOutOfStock
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-xs'
            }`}
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
