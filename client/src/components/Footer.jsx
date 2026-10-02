import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-100 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand & Description */}
          <div className="space-y-4 md:col-span-1">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="8" cy="21" r="1"/>
                  <circle cx="19" cy="21" r="1"/>
                  <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
                </svg>
              </div>
              <span className="text-lg font-bold text-gray-900">
                Mini<span className="text-indigo-600">Store</span>
              </span>
            </Link>
            <p className="text-sm text-gray-500 leading-relaxed">
              A modern, lightweight MERN stack e-commerce demonstration platform built with clean design and responsive performance.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">
              Shop & Explore
            </h4>
            <ul className="space-y-2.5 text-sm text-gray-600">
              <li>
                <Link to="/" className="hover:text-indigo-600 transition">Home</Link>
              </li>
              <li>
                <Link to="/products" className="hover:text-indigo-600 transition">All Products</Link>
              </li>
              <li>
                <Link to="/products?category=cat_1" className="hover:text-indigo-600 transition">Electronics</Link>
              </li>
              <li>
                <Link to="/products?category=cat_2" className="hover:text-indigo-600 transition">Fashion</Link>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">
              Account & Help
            </h4>
            <ul className="space-y-2.5 text-sm text-gray-600">
              <li>
                <Link to="/cart" className="hover:text-indigo-600 transition">Shopping Cart</Link>
              </li>
              <li>
                <Link to="/my-orders" className="hover:text-indigo-600 transition">My Orders</Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-indigo-600 transition">Sign In</Link>
              </li>
              <li>
                <Link to="/register" className="hover:text-indigo-600 transition">Create Account</Link>
              </li>
            </ul>
          </div>

          {/* Contact Details */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">
              Contact & Project
            </h4>
            <ul className="space-y-2.5 text-sm text-gray-600">
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>support@ministore.demo</span>
              </li>
              <li className="flex items-center gap-2">
                <svg className="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Pune, Maharashtra, India</span>
              </li>
              <li className="text-xs text-gray-400 pt-2">
                MERN Stack College Demo Project
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 mt-8 border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-400 gap-4">
          <p>© {new Date().getFullYear()} MiniStore Demo Project. All rights reserved.</p>
          <div className="flex gap-4">
            <span>Designed for College Presentation</span>
            <span>•</span>
            <span>React + Vite + Tailwind CSS</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
