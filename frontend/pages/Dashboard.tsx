import React, { useEffect, useState } from 'react';
import { Plus, Search, Trash2, Edit2, AlertTriangle, FileText } from 'lucide-react';
import { Layout } from '../components/Layout';
import { PatientModal } from '../components/PatientModal';
import { useAuth } from '../context/AuthContext';
import api  from '../services/api'; 
// import { mockBackend } from '../services/mockBackend'; // Switched to real API
import { Patient } from '../types';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export const Dashboard: React.FC = () => {
  const { token, user } = useAuth();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null);
  const [error, setError] = useState('');
  
  // Check if user is doctor (has permission to modify)
  const canModify = user?.role === 'doctor';

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    if (!token) {
      setError('No authentication token found');
      setIsLoading(false);
      return;
    }
    
    setIsLoading(true);
    setError('');
    try {
      const data = await api.fetchPatients(token);
      if (data) {
        setPatients(data);
      }
    } catch (err) {
      console.error(err);
      setError("Could not connect to the server. Is the Flask backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!token) return;
    
    if (window.confirm("Are you sure you want to delete this patient record? This action cannot be undone.")) {
      try {
        await api.deletePatient(id, token);
        fetchPatients();
      } catch (err) {
        alert("Failed to delete patient");
      }
    }
  };

  const handleEdit = (patient: Patient) => {
    setEditingPatient(patient);
    setIsModalOpen(true);
  };

  const handleAdd = () => {
    setEditingPatient(null);
    setIsModalOpen(true);
  };

  const handleModalSubmit = async (data: Omit<Patient, 'id'>) => {
    if (!token) return;
    
    try {
      if (editingPatient && editingPatient.id !== undefined) {
        await api.updatePatient(editingPatient.id, data, token);
      } else {
        await api.addPatient(data, token);
      }
      fetchPatients();
    } catch (err) {
      console.error("Failed to save", err);
      throw err; // Propagate to modal to show error
    }
  };

  const filteredPatients = patients.filter(p => 
    p.name?.toLowerCase().includes(searchTerm.toLowerCase()) || 
    p.gender?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.id?.toString().includes(searchTerm)
  );

  // Statistics
  const strokeStats = [
    { name: 'Stroke', value: patients.filter(p => p.stroke === 1 || p.stroke_prediction === 1).length },
    { name: 'No Stroke', value: patients.filter(p => p.stroke === 0 || p.stroke_prediction === 0 || !p.stroke_prediction).length },
  ];
  
  const genderStats = [
    { name: 'Male', value: patients.filter(p => p.gender === 'Male').length },
    { name: 'Female', value: patients.filter(p => p.gender === 'Female').length },
  ];

  return (
    <Layout>
      <div className="space-y-6">
        {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <AlertTriangle className="h-5 w-5 text-red-400" />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm text-red-700">
                            {error}
                        </p>
                    </div>
                </div>
            </div>
        )}

        {/* Header Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="text-sm font-medium text-gray-500">Total Patients</div>
            <div className="text-2xl font-bold text-gray-900 mt-2">{patients.length}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="text-sm font-medium text-gray-500">Avg Glucose Level</div>
            <div className="text-2xl font-bold text-gray-900 mt-2">
              {(patients.reduce((acc, p) => acc + p.avg_glucose_level, 0) / (patients.length || 1)).toFixed(1)}
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
             <div className="text-sm font-medium text-gray-500">Avg Age</div>
            <div className="text-2xl font-bold text-gray-900 mt-2">
               {(patients.reduce((acc, p) => acc + p.age, 0) / (patients.length || 1)).toFixed(1)}
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="text-sm font-medium text-gray-500">Stroke Risk Observed</div>
            <div className="text-2xl font-bold text-red-600 mt-2">
               {patients.filter(p => p.stroke === 1).length}
            </div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-80">
            <h3 className="text-lg font-medium text-gray-800 mb-4">Stroke Distribution</h3>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={strokeStats}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  fill="#8884d8"
                  paddingAngle={5}
                  dataKey="value"
                >
                  {strokeStats.map((entry, index) => (
                    <Cell key={`stroke-${entry.name}-${index}`} fill={index === 0 ? '#EF4444' : '#10B981'} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-80">
            <h3 className="text-lg font-medium text-gray-800 mb-4">Patient Demographics (Gender)</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={genderStats}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Action Bar */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="relative w-full sm:w-96">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search by name, ID or gender..."
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          {canModify && (
            <button
              onClick={handleAdd}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 w-full sm:w-auto"
            >
              <Plus className="-ml-1 mr-2 h-5 w-5" />
              Add Patient
            </button>
          )}
        </div>

        {/* Data Table */}
        <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Demographics</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Work/Residence</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Health Vitals</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Conditions</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  {canModify && <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {isLoading ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-12 text-center text-sm text-gray-500">
                      Loading patient records...
                    </td>
                  </tr>
                ) : filteredPatients.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-12 text-center text-sm text-gray-500">
                      No patients found matching your criteria.
                    </td>
                  </tr>
                ) : (
                  filteredPatients.map((patient) => (
                    <tr key={patient.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{patient.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div className="font-medium text-gray-900">{patient.name}</div>
                        <div>{patient.age} yrs • {patient.gender}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div>{patient.work_type.replace('_', ' ')}</div>
                        <div className="text-xs text-gray-400">{patient.residence_type}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div>BMI: {patient.bmi}</div>
                        <div>Glu: {patient.avg_glucose_level}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                         <div className="flex gap-1">
                           {patient.hypertension === 1 && <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">Hyp</span>}
                           {patient.heart_disease === 1 && <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">Heart</span>}
                           {patient.hypertension === 0 && patient.heart_disease === 0 && <span className="text-gray-400">-</span>}
                         </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {patient.stroke === 1 ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                            Stroke
                          </span>
                        ) : (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            Healthy
                          </span>
                        )}
                      </td>
                      {canModify && (
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button onClick={() => handleEdit(patient)} className="text-blue-600 hover:text-blue-900 mr-4">
                            <Edit2 size={18} />
                          </button>
                          <button onClick={() => handleDelete(patient.id)} className="text-red-600 hover:text-red-900">
                            <Trash2 size={18} />
                          </button>
                        </td>
                      )}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <PatientModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleModalSubmit}
        initialData={editingPatient}
      />
    </Layout>
  );
};