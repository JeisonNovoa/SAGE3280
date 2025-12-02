import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Patients from './pages/Patients';
import PatientDetail from './pages/PatientDetail';
import PriorityList from './pages/PriorityList';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="upload" element={<Upload />} />
        <Route path="patients" element={<Patients />} />
        <Route path="patients/:id" element={<PatientDetail />} />
        <Route path="priority" element={<PriorityList />} />
      </Route>
    </Routes>
  );
}

export default App;
