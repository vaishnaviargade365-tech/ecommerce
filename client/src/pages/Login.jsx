import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email.trim() || !password) {
      setError('Please fill in both email and password.');
      return;
    }

    try {
      setLoading(true);
      const res = await login(email, password);

      if (res.success) {
        showToast(`Welcome back, ${res.user.name}!`, 'success');

        // Redirect admin to dashboard, customer to previous page or home
        if (res.user.role === 'admin') {
          navigate('/admin');
        } else {
          navigate(from === '/login' ? '/' : from);
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  // Demo auto-fill helpers for presentation convenience
  const fillDemo = (demoType) => {
    if (demoType === 'admin') {
      setEmail('admin@demo.com');
      setPassword('admin123');
    } else {
      setEmail('customer@demo.com');
      setPassword('password123');
    }
    setError('');
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full bg-white rounded-3xl p-8 sm:p-10 border border-gray-100 shadow-xl space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <Link to="/" className="inline-flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-200">
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <circle cx="8" cy="21" r="1"/>
                <circle cx="19" cy="21" r="1"/>
                <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>
              </svg>
            </div>
            <span className="text-xl font-bold text-gray-900">
              Mini<span className="text-indigo-600">Store</span>
            </span>
          </Link>
          <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Sign In to Your Account</h2>
          <p className="text-xs text-gray-500">
            Access your shopping cart, order history, and account settings
          </p>
        </div>

        {/* Demo Fast-Login Notice */}
        <div className="p-3.5 bg-indigo-50/70 border border-indigo-100 rounded-2xl text-xs space-y-2">
          <div className="flex items-center justify-between text-indigo-900 font-semibold">
            <span>⚡ Demo Quick-Fill:</span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => fillDemo('customer')}
              className="py-1.5 px-2.5 bg-white hover:bg-indigo-50 border border-indigo-200 rounded-lg text-indigo-700 font-medium transition text-center shadow-2xs"
            >
              Customer Demo
            </button>
            <button
              type="button"
              onClick={() => fillDemo('admin')}
              className="py-1.5 px-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition text-center shadow-2xs"
            >
              Admin Demo
            </button>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-3.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-2xl text-xs font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. customer@demo.com"
              className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-600 transition"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-6 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-2xl shadow-lg shadow-indigo-200 transition text-sm flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Signing in...</span>
              </>
            ) : (
              <span>Sign In</span>
            )}
          </button>
        </form>

        {/* Footer links */}
        <div className="pt-4 border-t border-gray-100 text-center space-y-3 text-xs">
          <p className="text-gray-500">
            Don't have an account?{' '}
            <Link to="/register" className="font-semibold text-indigo-600 hover:text-indigo-700">
              Create an account
            </Link>
          </p>
          <div>
            <Link to="/" className="text-gray-400 hover:text-gray-600 transition">
              ← Return to store
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
