import React from 'react';
import { useAuth } from '../context/AuthContext';
import { LogOut, Activity, User, ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900 tracking-tight">
                Neuro<span className="text-blue-600">Guard</span>
              </span>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center text-sm text-gray-500">
                <ShieldCheck className="w-4 h-4 mr-1 text-green-500" />
                <span>Secure Environment</span>
              </div>
              <div className="h-6 w-px bg-gray-200 mx-2 hidden md:block"></div>
              <div className="flex items-center gap-3">
                <div className="flex flex-col items-end">
                  <span className="text-sm font-medium text-gray-700">{user?.username}</span>
                  <span className="text-xs text-gray-500 uppercase">{user?.role}</span>
                </div>
                <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                  <User size={18} />
                </div>
                <button 
                  onClick={handleLogout}
                  className="ml-2 p-2 text-gray-400 hover:text-red-500 transition-colors"
                  title="Logout"
                >
                  <LogOut size={20} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      <footer className="bg-white border-t border-gray-200 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>&copy; 2024 NeuroGuard Medical Systems. Secure & HIPAA Compliant.</p>
        </div>
      </footer>
    </div>
  );
};