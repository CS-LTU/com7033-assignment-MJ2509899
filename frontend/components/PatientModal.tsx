import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { Patient, Gender, WorkType, ResidenceType, SmokingStatus } from '../types';

interface PatientModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (patient: Omit<Patient, 'id'>) => Promise<void>;
  initialData?: Patient | null;
}

const INITIAL_FORM: Omit<Patient, 'id'> = {
  name: '',
  gender: Gender.Male,
  age: 50,
  hypertension: 0,
  heart_disease: 0,
  ever_married: "Yes",
  work_type: WorkType.Private,
  residence_type: ResidenceType.Urban,
  avg_glucose_level: 100,
  bmi: 25,
  smoking_status: SmokingStatus.NeverSmoked,
  stroke: 0
};

export const PatientModal: React.FC<PatientModalProps> = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState<Omit<Patient, 'id'>>(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialData) {
      const { id, ...rest } = initialData;
      setFormData(rest);
    } else {
      setFormData(INITIAL_FORM);
    }
    setError('');
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await onSubmit(formData);
      onClose();
    } catch (err) {
      setError('Failed to save patient. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof Omit<Patient, 'id'>, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">
            {initialData ? 'Edit Patient Record' : 'Add New Patient'}
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && <div className="text-red-600 bg-red-50 p-3 rounded text-sm">{error}</div>}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Basic Info */}
            <div className="space-y-4">
              <h3 className="font-semibold text-gray-700 border-b pb-2">Demographics</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Patient Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={e => handleChange('name', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                  placeholder="Enter patient name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Age</label>
                <input
                  type="number"
                  required
                  min="0"
                  max="120"
                  value={formData.age}
                  onChange={e => handleChange('age', Number(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Gender</label>
                <select
                  value={formData.gender}
                  onChange={e => handleChange('gender', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                >
                  {Object.values(Gender).map(g => <option key={g} value={g}>{g}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Work Type</label>
                <select
                  value={formData.work_type}
                  onChange={e => handleChange('work_type', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                >
                  {Object.values(WorkType).map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>

               <div>
                <label className="block text-sm font-medium text-gray-700">Residence Type</label>
                <select
                  value={formData.residence_type}
                  onChange={e => handleChange('residence_type', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                >
                  {Object.values(ResidenceType).map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
               <div>
                <label className="block text-sm font-medium text-gray-700">Ever Married?</label>
                <select
                  value={formData.ever_married}
                  onChange={e => handleChange('ever_married', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>

            {/* Medical Info */}
            <div className="space-y-4">
              <h3 className="font-semibold text-gray-700 border-b pb-2">Medical History</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">BMI</label>
                <input
                  type="number"
                  step="0.1"
                  required
                  value={formData.bmi}
                  onChange={e => handleChange('bmi', Number(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Avg Glucose Level</label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={formData.avg_glucose_level}
                  onChange={e => handleChange('avg_glucose_level', Number(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Smoking Status</label>
                <select
                  value={formData.smoking_status}
                  onChange={e => handleChange('smoking_status', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                >
                  {Object.values(SmokingStatus).map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              <div className="flex gap-4 mt-6">
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.hypertension === 1}
                    onChange={e => handleChange('hypertension', e.target.checked ? 1 : 0)}
                    className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                  />
                  <span className="text-sm text-gray-700">Hypertension</span>
                </label>

                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.heart_disease === 1}
                    onChange={e => handleChange('heart_disease', e.target.checked ? 1 : 0)}
                    className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                  />
                  <span className="text-sm text-gray-700">Heart Disease</span>
                </label>
              </div>

              <div className="bg-red-50 p-3 rounded-md border border-red-100 mt-4">
                 <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.stroke === 1}
                    onChange={e => handleChange('stroke', e.target.checked ? 1 : 0)}
                    className="rounded text-red-600 focus:ring-red-500 h-4 w-4"
                  />
                  <span className="text-sm font-bold text-red-700">Prior Stroke Incident</span>
                </label>
              </div>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save Record'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};