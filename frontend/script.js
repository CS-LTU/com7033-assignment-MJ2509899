// This file handles all front-end logic and communicates with the Flask API

const API_BASE = '/api/patients';
const LOGIN_API = '/login';

// --- Global State ---
let userRole = sessionStorage.getItem('hms_role');
let userId = sessionStorage.getItem('hms_user');

// Permissions mapping (Mirrors the Python back-end for front-end UI control)
const permissions = {
  'administrator': { canView: true, canAdd: true, canEdit: true, canDelete: true },
  'doctor': { canView: true, canAdd: true, canEdit: false, canDelete: false }, 
  'viewer': { canView: true, canAdd: false, canEdit: false, canDelete: false },
};

const getCurrentPermissions = () => permissions[userRole] || permissions.viewer;


// --- CORE CRUD FUNCTIONS (API Calls) ---

// READ: Fetches patient data from the back-end
const fetchAndRenderPatients = async (searchQuery = '') => {
  const tableBody = document.getElementById('patientTableBody');
  tableBody.innerHTML = '<tr><td colspan="6" class="text-center">Loading patient data...</td></tr>';
  
  const userPerms = getCurrentPermissions(); 
  
  if (!userPerms.canView) {
    tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Permission Denied: Cannot view records.</td></tr>';
    return;
  }

  try {
    // Send role in the query parameter for the back-end check
    const response = await fetch(`${API_BASE}?role=${userRole}`); 
    if (!response.ok) throw new Error('Failed to fetch patients.');
    
    let patients = await response.json();
    
    // Client-side filtering
    const filteredPatients = patients.filter((p) => 
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
      p.id.toLowerCase().includes(searchQuery.toLowerCase())
    );

    tableBody.innerHTML = ''; // Clear loading message

    if (filteredPatients.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No records found.</td></tr>';
    }

    filteredPatients.forEach((patient) => {
      const row = tableBody.insertRow();
      
      let actionButtons = '';
      if (userPerms.canEdit) {
        actionButtons += `<button class="btn btn-sm btn-info me-1 edit-btn" data-id="${patient.id}">View/Edit</button>`;
      }
      if (userPerms.canDelete) {
        actionButtons += `<button class="btn btn-sm btn-danger delete-btn" data-id="${patient.id}">Discharge</button>`;
      }
      if (!actionButtons) {
          actionButtons = '<span class="text-muted">No Actions</span>';
      }

      row.innerHTML = `
        <td>${patient.id}</td>
        <td>${patient.name}</td>
        <td>${patient.dob}</td>
        <td>${patient.ward}</td>
        <td>${patient.admissionDate}</td>
        <td>${actionButtons}</td>
      `;
    });
  } catch (error) {
    console.error('Error fetching patients:', error);
    tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error connecting to the API or database.</td></tr>';
  }
};

// CREATE/UPDATE: Handles form submission
const handleFormSubmission = async (e) => {
  e.preventDefault();
  
  const isUpdate = !!document.getElementById('patientId').value;
  const userPerms = getCurrentPermissions();
  
  if (isUpdate && !userPerms.canEdit) {
    alert('Permission Denied: You cannot update records.');
    return;
  }
  if (!isUpdate && !userPerms.canAdd) {
    alert('Permission Denied: You cannot add new records.');
    return;
  }
  
  const patientId = document.getElementById('patientId').value;
  
  const newRecord = {
    role: userRole, // Send role for back-end permission check
    name: document.getElementById('patientName').value,
    dob: document.getElementById('patientDOB').value,
    gender: document.getElementById('patientGender').value,
    address: document.getElementById('patientAddress').value,
    ward: document.getElementById('patientWard').value,
    admissionDate: document.getElementById('admissionDate').value,
    doctor: document.getElementById('referringDoctor').value,
  };
  
  const method = isUpdate ? 'PUT' : 'POST';
  const url = isUpdate ? `${API_BASE}/${patientId}` : API_BASE;

  try {
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newRecord),
    });

    const result = await response.json();
    
    if (!response.ok) {
      alert(`Operation Failed: ${result.message || response.statusText}`);
      return;
    }
    
    alert(result.message);

    fetchAndRenderPatients('');
    resetPatientForm();
    document.getElementById('view-tab').click();
    
  } catch (error) {
    console.error('Submission error:', error);
    alert('An unexpected error occurred during submission.');
  }
};

// DELETE: Handles patient deletion
const deletePatient = async (patientId) => {
  const userPerms = getCurrentPermissions();
  if (!userPerms.canDelete) {
    alert('Permission Denied: You cannot discharge/delete records.');
    return;
  }
  
  if (!confirm(`Are you sure you want to discharge patient ${patientId}? This cannot be undone.`)) {
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/${patientId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: userRole }), // Send role for back-end check
    });

    const result = await response.json();

    if (!response.ok) {
      alert(`Deletion Failed: ${result.message || response.statusText}`);
      return;
    }

    alert(result.message);
    fetchAndRenderPatients('');
  } catch (error) {
    console.error('Deletion error:', error);
    alert('An unexpected error occurred during deletion.');
  }
};


// --- UTILITY FUNCTIONS ---

const resetPatientForm = () => {
  document.getElementById('patientForm').reset();
  document.getElementById('patientId').value = '';
  document.getElementById('formTitle').textContent = 'Add New Patient Record';
  document.getElementById('formTitle').classList.remove('edit-form-heading');
  document.getElementById('savePatientBtn').textContent = 'Save New Record';
  document.getElementById('cancelEditBtn').style.display = 'none';
};

// Populate the form for editing (requires reading data first)
const populateFormForEdit = async (patientId) => {
  const userPerms = getCurrentPermissions();
  if (!userPerms.canEdit) {
    alert('Permission Denied: You cannot open the form for editing.');
    return;
  }

  // Fetch all patients and find the one to edit
  try {
    const response = await fetch(`${API_BASE}?role=${userRole}`);
    const patients = await response.json();
    const patient = patients.find((p) => p.id === patientId);

    if (!patient) {
        alert('Patient record not found.');
        return;
    }
    
    // Set hidden ID for update logic
    document.getElementById('patientId').value = patient.id; 
    
    // Populate fields
    document.getElementById('patientName').value = patient.name;
    document.getElementById('patientDOB').value = patient.dob;
    document.getElementById('patientGender').value = patient.gender;
    document.getElementById('patientAddress').value = patient.address;
    document.getElementById('patientWard').value = patient.ward;
    document.getElementById('admissionDate').value = patient.admissionDate;
    document.getElementById('referringDoctor').value = patient.doctor;

    // Update UI for Edit mode
    document.getElementById('formTitle').textContent = `Editing Patient Record: ${patient.id}`;
    document.getElementById('formTitle').classList.add('edit-form-heading');
    document.getElementById('savePatientBtn').textContent = 'Update Record';
    document.getElementById('cancelEditBtn').style.display = 'inline-block';
    
    // Switch to the form tab
    document.getElementById('add-tab').click();
    
  } catch (error) {
    console.error('Error fetching data for edit:', error);
    alert('Could not load patient data for editing.');
  }
};

const updateUIToReflectRole = () => {
    const userPerms = getCurrentPermissions();
    const addTab = document.getElementById('add-tab').parentElement;

    if (userPerms.canAdd || userPerms.canEdit) {
        addTab.style.display = 'block';
    } else {
        addTab.style.display = 'none';
        document.getElementById('view-tab').click();
    }
    
    fetchAndRenderPatients(''); 
};


// --- EVENT LISTENERS (The glue) ---

document.addEventListener('DOMContentLoaded', () => {
  
  // Check login state on load and initialize UI
  if (userRole) {
    document.getElementById('loggedInUser').textContent = `${userRole.toUpperCase()} (${userId})`;
    document.getElementById('login-view').style.display = 'none';
    document.getElementById('dashboard-view').style.display = 'block';
    updateUIToReflectRole();
  }

  // 1. Login Handler
  document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputUserId = document.getElementById('userId').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(LOGIN_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId: inputUserId, password }),
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Successful login: Store user ID and ROLE
            userId = inputUserId;
            userRole = result.role;
            sessionStorage.setItem('hms_user', userId);
            sessionStorage.setItem('hms_role', userRole);
            
            document.getElementById('loggedInUser').textContent = `${userRole.toUpperCase()} (${userId})`;
            document.getElementById('login-view').style.display = 'none';
            document.getElementById('dashboard-view').style.display = 'block';
            
            updateUIToReflectRole(); 
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert('Could not connect to the server.');
    }
  });

  // 2. Logout Handler
  document.getElementById('logoutBtn').addEventListener('click', () => {
    sessionStorage.removeItem('hms_user');
    sessionStorage.removeItem('hms_role');
    userId = null;
    userRole = null;
    document.getElementById('dashboard-view').style.display = 'none';
    document.getElementById('login-view').style.display = 'flex';
    document.getElementById('loginForm').reset();
  });

  // 3. Form Submission (Create/Update) Handler
  document.getElementById('patientForm').addEventListener('submit', handleFormSubmission);
  
  // 4. Cancel Edit Handler
  document.getElementById('cancelEditBtn').addEventListener('click', resetPatientForm);

  // 5. Delete and Edit Button Handler (Delegation)
  document.getElementById('patientTableBody').addEventListener('click', (e) => {
    const patientId = e.target.getAttribute('data-id');
    if (!patientId) return;

    if (e.target.classList.contains('delete-btn')) {
      deletePatient(patientId);
    } else if (e.target.classList.contains('edit-btn')) {
      populateFormForEdit(patientId);
    }
  });
  
  // 6. Search Handler
  document.getElementById('searchPatientBtn').addEventListener('click', () => {
    const query = document.getElementById('searchPatientInput').value;
    fetchAndRenderPatients(query);
  });
});