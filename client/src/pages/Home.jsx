import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import { initialProducts, initialCategories } from '../data/mockData';
import api from '../api/axios';

const Home = () => {
  const [products, setProducts] = useState(initialProducts);
  const [categories, setCategories] = useState(initialCategories);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Attempt real API fetch if available, fallback to mock data
    const fetchData = async () => {
      try {
        setLoading(true);
        const [prodRes, catRes] = await Promise.all([
          api.get('/products'),
          api.get('/categories'),
        ]);
        if (prodRes.data && prodRes.data.length > 0) setProducts(prodRes.data);
        if (catRes.data && catRes.data.length > 0) setCategories(catRes.data);
      } catch (err) {
        // Fallback to local mock data automatically
        console.log('Using mock catalog data for demo');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const featuredProducts = products.slice(0, 4);

  return (
    <div className="space-y-16 pb-16">
      {/* 1. Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-indigo-900 via-indigo-800 to-indigo-950 text-white rounded-3xl mx-4 sm:mx-6 lg:mx-8 mt-6 p-8 sm:p-12 lg:p-16 shadow-xl">
        <div className="relative z-10 max-w-2xl">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/30 text-indigo-200 border border-indigo-400/30 mb-6">
            ✨ Mini E-Commerce Demo Platform
          </span>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight mb-6">
            Discover Quality Essentials for Modern Living.
          </h1>
          <p className="text-indigo-100 text-base sm:text-lg mb-8 leading-relaxed max-w-xl">
            Explore curated collections of top-tier electronics, modern apparel, footwear, and home goods with effortless checkout and Cash on Delivery.
          </p>
          <div className="flex flex-wrap items-center gap-4">
            <Link
              to="/products"
              className="px-6 py-3.5 bg-white text-indigo-900 hover:bg-indigo-50 font-bold rounded-2xl shadow-lg transition transform hover:-translate-y-0.5 text-sm sm:text-base"
            >
              Shop All Products
            </Link>
            <Link
              to="/products?category=cat_1"
              className="px-6 py-3.5 bg-indigo-700/50 hover:bg-indigo-700/80 text-white font-medium rounded-2xl border border-indigo-400/30 transition text-sm sm:text-base backdrop-blur-sm"
            >
              View Electronics
            </Link>
          </div>
        </div>

        {/* Decorative background glow & shapes */}
        <div className="absolute right-0 top-0 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>
        <div className="absolute right-10 bottom-10 hidden lg:block opacity-20 pointer-events-none">
          <svg className="w-80 h-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="0.5">
            <circle cx="8" cy="21" r="1"/>
            <circle cx="19" cy="21" r="1"/>
            <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
          </svg>
        </div>
      </section>

      {/* 2. Featured Categories Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 tracking-tight">Featured Categories</h2>
            <p className="text-sm text-gray-500 mt-1">Browse through our most popular departments</p>
          </div>
          <Link to="/products" className="text-sm font-semibold text-indigo-600 hover:text-indigo-700 transition">
            All categories →
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat._id}
              to={`/products?category=${cat._id}`}
              className="group p-5 bg-white rounded-2xl border border-gray-100 shadow-xs hover:shadow-md hover:border-indigo-100 transition text-center flex flex-col items-center justify-center gap-2"
            >
              <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
              </div>
              <span className="font-semibold text-gray-900 text-sm group-hover:text-indigo-600 transition-colors">
                {cat.name}
              </span>
              <span className="text-[11px] text-gray-400 line-clamp-1">{cat.description}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* 3. Featured Products Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 tracking-tight">Trending Products</h2>
            <p className="text-sm text-gray-500 mt-1">Handpicked best-sellers ready to ship</p>
          </div>
          <Link to="/products" className="text-sm font-semibold text-indigo-600 hover:text-indigo-700 transition">
            See entire catalog →
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-72 bg-gray-100 rounded-2xl animate-pulse"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product) => (
              <ProductCard key={product._id} product={product} />
            ))}
          </div>
        )}
      </section>

      {/* 4. Why Choose Us Section */}
      <section className="bg-white border-y border-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl font-bold text-gray-900">Why Shop With MiniStore?</h2>
            <p className="text-sm text-gray-500 mt-2">
              Designed from the ground up to ensure a smooth, worry-free shopping journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="p-6 bg-gray-50 rounded-2xl text-center">
              <div className="w-12 h-12 mx-auto rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 text-base mb-1">Secure Shopping</h3>
              <p className="text-xs text-gray-500 leading-relaxed">
                Protected authentication and verified database price calculations.
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-2xl text-center">
              <div className="w-12 h-12 mx-auto rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 text-base mb-1">Fast Delivery</h3>
              <p className="text-xs text-gray-500 leading-relaxed">
                Prompt dispatch and real-time status tracking on every order.
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-2xl text-center">
              <div className="w-12 h-12 mx-auto rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 text-base mb-1">Quality Products</h3>
              <p className="text-xs text-gray-500 leading-relaxed">
                Hand-tested products from top categories with authentic specifications.
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-2xl text-center">
              <div className="w-12 h-12 mx-auto rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900 text-base mb-1">Easy COD Checkout</h3>
              <p className="text-xs text-gray-500 leading-relaxed">
                Simple Cash on Delivery checkout with zero complex gateway hassle.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Call-To-Action Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-indigo-600 to-indigo-800 rounded-3xl p-8 sm:p-12 text-center text-white shadow-lg">
          <h2 className="text-2xl sm:text-3xl font-extrabold mb-4">Ready to Start Shopping?</h2>
          <p className="text-indigo-100 text-sm sm:text-base max-w-xl mx-auto mb-8">
            Experience our responsive customer shopping flow from product search all the way to Cash on Delivery placement.
          </p>
          <Link
            to="/products"
            className="inline-block px-8 py-3.5 bg-white text-indigo-700 hover:bg-indigo-50 font-bold rounded-2xl shadow-md transition"
          >
            Explore All Products Now
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
