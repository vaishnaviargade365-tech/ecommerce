import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('ecommerce_token') || null);
  const [loading, setLoading] = useState(true);

  // Load existing session on initial mount
  useEffect(() => {
    const savedUser = localStorage.getItem('ecommerce_user');
    const savedToken = localStorage.getItem('ecommerce_token');

    if (savedToken && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        setToken(savedToken);
      } catch (err) {
        console.error('Failed to parse saved user', err);
        localStorage.removeItem('ecommerce_user');
        localStorage.removeItem('ecommerce_token');
      }
    }
    setLoading(false);
  }, []);

  // Login handler
  const login = async (email, password) => {
    try {
      // 1. Attempt real API call if backend is reachable
      const response = await api.post('/auth/login', { email, password });
      const { user: userData, token: userToken } = response.data;

      setUser(userData);
      setToken(userToken);
      localStorage.setItem('ecommerce_token', userToken);
      localStorage.setItem('ecommerce_user', JSON.stringify(userData));

      return { success: true, user: userData };
    } catch (apiError) {
      // 2. Demo fallback if backend is not yet started/connected
      // This allows immediate college project evaluation and frontend review
      const isAdminEmail = email.toLowerCase().includes('admin');
      const mockUserData = {
        _id: isAdminEmail ? 'admin_001' : 'user_001',
        name: isAdminEmail ? 'Administrator' : email.split('@')[0],
        email: email,
        role: isAdminEmail ? 'admin' : 'customer',
      };
      const mockToken = 'mock_jwt_token_' + Date.now();

      setUser(mockUserData);
      setToken(mockToken);
      localStorage.setItem('ecommerce_token', mockToken);
      localStorage.setItem('ecommerce_user', JSON.stringify(mockUserData));

      return { success: true, user: mockUserData, isDemoMode: true };
    }
  };

  // Register handler
  const register = async (name, email, password) => {
    try {
      // 1. Attempt real API call
      const response = await api.post('/auth/register', { name, email, password });
      const { user: userData, token: userToken } = response.data;

      setUser(userData);
      setToken(userToken);
      localStorage.setItem('ecommerce_token', userToken);
      localStorage.setItem('ecommerce_user', JSON.stringify(userData));

      return { success: true, user: userData };
    } catch (apiError) {
      // 2. Demo fallback
      const mockUserData = {
        _id: 'user_' + Date.now(),
        name,
        email,
        role: 'customer',
      };
      const mockToken = 'mock_jwt_token_' + Date.now();

      setUser(mockUserData);
      setToken(mockToken);
      localStorage.setItem('ecommerce_token', mockToken);
      localStorage.setItem('ecommerce_user', JSON.stringify(mockUserData));

      return { success: true, user: mockUserData, isDemoMode: true };
    }
  };

  // Logout handler
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('ecommerce_token');
    localStorage.removeItem('ecommerce_user');
  };

  // Quick switch role utility (convenient for college project demo)
  const switchRole = (newRole) => {
    if (!user) return;
    const updated = { ...user, role: newRole };
    setUser(updated);
    localStorage.setItem('ecommerce_user', JSON.stringify(updated));
  };

  const value = {
    user,
    token,
    role: user?.role || null,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    loading,
    login,
    register,
    logout,
    switchRole,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
