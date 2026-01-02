import { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Home, Upload, Users as UsersIcon, Activity, ListTodo, Settings, UserCog, Shield, FileText } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import UserMenu from './UserMenu';
import PermissionGuard from './PermissionGuard';
import PasswordChangeModal from './PasswordChangeModal';

const Layout = () => {
  const location = useLocation();
  const { hasPermission, hasRole } = useAuth();
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  // Definir navegación con permisos requeridos
  const navigationItems = [
    {
      name: 'Dashboard',
      href: '/',
      icon: Home,
      // Todos los usuarios autenticados pueden ver el dashboard
    },
    {
      name: 'Cargar Excel',
      href: '/upload',
      icon: Upload,
      permission: 'upload.create'
    },
    {
      name: 'Pacientes',
      href: '/patients',
      icon: UsersIcon,
      // Todos los usuarios autenticados pueden ver pacientes
    },
    {
      name: 'Lista de Prioridad',
      href: '/priority',
      icon: ListTodo,
      // Todos los usuarios autenticados pueden ver la lista de prioridad
    },
    {
      name: 'Administración',
      href: '/admin',
      icon: Settings,
      role: 'admin'
    },
    {
      name: 'Usuarios',
      href: '/users',
      icon: UserCog,
      permission: 'users.read'
    },
    {
      name: 'Roles',
      href: '/roles',
      icon: Shield,
      permission: 'roles.read'
    },
    {
      name: 'Auditoría',
      href: '/audit',
      icon: FileText,
      permission: 'audit.read'
    },
  ];

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  // Filtrar navegación según permisos del usuario
  const allowedNavigation = navigationItems.filter(item => {
    // Si no tiene restricciones, permitir
    if (!item.permission && !item.role) {
      return true;
    }

    // Verificar permiso
    if (item.permission && !hasPermission(item.permission)) {
      return false;
    }

    // Verificar rol
    if (item.role && !hasRole(item.role)) {
      return false;
    }

    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-blue-600" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">
                SAGE<span className="text-blue-600">3280</span>
              </h1>
            </div>

            {/* User Menu */}
            <UserMenu onChangePassword={() => setShowPasswordModal(true)} />
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {allowedNavigation.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.href);

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center px-3 py-4 text-sm font-medium border-b-2 transition-colors
                    ${active
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }
                  `}
                >
                  <Icon className="h-5 w-5 mr-2" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            © 2024 SAGE3280. Sistema de Gestión de Atención Primaria en Salud - Resolución 3280
          </p>
        </div>
      </footer>

      {/* Password Change Modal */}
      {showPasswordModal && (
        <PasswordChangeModal
          isOpen={showPasswordModal}
          onClose={() => setShowPasswordModal(false)}
        />
      )}
    </div>
  );
};

export default Layout;
