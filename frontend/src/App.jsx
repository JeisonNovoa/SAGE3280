import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import ErrorBoundary from './components/ErrorBoundary';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Patients from './pages/Patients';
import PatientDetail from './pages/PatientDetail';
import PriorityList from './pages/PriorityList';
import Admin from './pages/Admin';
import Users from './pages/Users';
import UserForm from './pages/UserForm';
import Roles from './pages/Roles';
import RoleForm from './pages/RoleForm';
import AuditLogs from './pages/AuditLogs';

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Routes>
        {/* Ruta pública - Login */}
        <Route path="/login" element={<Login />} />

        {/* Rutas protegidas con Layout */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          {/* Dashboard - Acceso para todos los usuarios autenticados */}
          <Route index element={<Dashboard />} />

          {/* Upload - Requiere permiso upload.create */}
          <Route
            path="upload"
            element={
              <ProtectedRoute requiredPermission="upload.create">
                <Upload />
              </ProtectedRoute>
            }
          />

          {/* Patients - Acceso para todos los usuarios autenticados */}
          <Route path="patients" element={<Patients />} />
          <Route path="patients/:id" element={<PatientDetail />} />

          {/* Priority List - Acceso para todos los usuarios autenticados */}
          <Route path="priority" element={<PriorityList />} />

          {/* Admin - Solo administradores */}
          <Route
            path="admin"
            element={
              <ProtectedRoute requiredRole="admin">
                <Admin />
              </ProtectedRoute>
            }
          />

          {/* Users Management - Requiere permiso users.read */}
          <Route
            path="users"
            element={
              <ProtectedRoute requiredPermission="users.read">
                <Users />
              </ProtectedRoute>
            }
          />
          <Route
            path="users/new"
            element={
              <ProtectedRoute requiredPermission="users.create">
                <UserForm />
              </ProtectedRoute>
            }
          />
          <Route
            path="users/:id/edit"
            element={
              <ProtectedRoute requiredPermission="users.update">
                <UserForm />
              </ProtectedRoute>
            }
          />

          {/* Roles Management - Requiere permiso roles.read */}
          <Route
            path="roles"
            element={
              <ProtectedRoute requiredPermission="roles.read">
                <Roles />
              </ProtectedRoute>
            }
          />
          <Route
            path="roles/new"
            element={
              <ProtectedRoute requiredPermission="roles.create">
                <RoleForm />
              </ProtectedRoute>
            }
          />
          <Route
            path="roles/:id/edit"
            element={
              <ProtectedRoute requiredPermission="roles.update">
                <RoleForm />
              </ProtectedRoute>
            }
          />

          {/* Audit Logs - Requiere permiso audit.read */}
          <Route
            path="audit"
            element={
              <ProtectedRoute requiredPermission="audit.read">
                <AuditLogs />
              </ProtectedRoute>
            }
          />
        </Route>

        {/* Redirect any unknown route to dashboard */}
        <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
