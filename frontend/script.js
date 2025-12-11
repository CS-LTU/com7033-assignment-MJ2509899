// Function to load and save data from/to localStorage
const storageKey = 'hms_patients';

const loadPatients = () => {
  const data = localStorage.getItem(storageKey);
  return data ? JSON.parse(data) : initializeSampleData();
};

const savePatients = (patients) => {
  localStorage.setItem(storageKey, JSON.stringify(patients));
};

// --- USER/ROLE SETUP ---
const userRoles = {
  // Credentials and their associated role
  'admin': { password: '1234', role: 'administrator' },
  'doctor': { password: 'pass', role: 'doctor' },
  'user': { password: 'view', role: 'viewer' },
};

// Permissions mapping
const permissions = {
  'administrator': { canView: true, canAdd: true, canEdit: true, canDelete: true },
  'doctor': { canView: true, canAdd: true, canEdit: false, canDelete: false }, // Doctors can view and add, but not edit/delete existing records here
  'viewer': { canView: true, canAdd: false, canEdit: false, canDelete: false },
};

const getCurrentRole = () => sessionStorage.getItem('hms_role');
const getCurrentPermissions = () => permissions[getCurrentRole()] || permissions.viewer;


// Initial data for a clean start
const initializeSampleData = () => {
  const initialPatients = [
    {
      id: 'P00123',
      name: 'Jane Doe',
      dob: '1985-04-21',
      gender: 'female',
      address: '10 Downing St',
      ward: 'General',
      admissionDate: '2025-11-20',
      doctor: 'Dr. Lee',
    },
    {
      id: 'P00456',
      name: 'John Smith',
      dob: '1992-07-15',
      gender: 'male',
      address: '42 Wallaby Way',
      ward: 'ICU',
      admissionDate: '2025-12-01',
      doctor: 'Dr. Chen',
    },
  ];
  savePatients(initialPatients);
  return initialPatients;
};

// --- CORE CRUD & UI FUNCTIONS ---

// READ: Renders the patient table, now adjusting buttons based on role
const renderPatientTable = (searchQuery = '') => {
  const patients = loadPatients();
  const tableBody = document.getElementById('patientTableBody');
  tableBody.innerHTML = ''; 
  const userPerms = getCurrentPermissions(); // Get permissions for the current user

  const filteredPatients = patients.filter((p) => 
    p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    p.id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  filteredPatients.forEach((patient) => {
    const row = tableBody.insertRow();
    
    // Build the actions column based on permissions
    let actionButtons = '';
    if (userPerms.canEdit) {
      actionButtons += `<button class="btn btn-sm btn-info me-1 edit-btn" data-id="${patient.id}">View/Edit</button>`;
    }
    if (userPerms.canDelete) {
      actionButtons += `<button class="btn btn-sm btn-danger delete-btn" data-id="${patient.id}">Discharge</button>`;
    }
    if (!userPerms.canEdit && !userPerms.canDelete) {
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
};

// CREATE/UPDATE: Handles form submission (only available to allowed roles)
const handleFormSubmission = (e) => {
  e.preventDefault();
  
  const userPerms = getCurrentPermissions();
  const isUpdate = !!document.getElementById('patientId').value;
  
  // Check permission before proceeding
  if (isUpdate && !userPerms.canEdit) {
    alert('Permission Denied: You cannot update records.');
    return;
  }
  if (!isUpdate && !userPerms.canAdd) {
    alert('Permission Denied: You cannot add new records.');
    return;
  }
  
  let patients = loadPatients();

  const newRecord = {
    id: isUpdate ? document.getElementById('patientId').value : generatePatientId(patients),
    name: document.getElementById('patientName').value,
    dob: document.getElementById('patientDOB').value,
    gender: document.getElementById('patientGender').value,
    address: document.getElementById('patientAddress').value,
    ward: document.getElementById('patientWard').value,
    admissionDate: document.getElementById('admissionDate').value,
    doctor: document.getElementById('referringDoctor').value,
  };

  if (isUpdate) {
    patients = patients.map((p) => (p.id === newRecord.id ? newRecord : p));
    alert(`Patient ${newRecord.id} updated successfully!`);
  } else {
    patients.push(newRecord);
    alert(`New patient ${newRecord.id} added successfully!`);
  }

  savePatients(patients);
  renderPatientTable('');
  resetPatientForm();
  document.getElementById('view-tab').click();
};

// DELETE: Handles patient deletion (only available to allowed roles)
const deletePatient = (patientId) => {
  const userPerms = getCurrentPermissions();
  if (!userPerms.canDelete) {
    alert('Permission Denied: You cannot discharge/delete records.');
    return;
  }
  
  if (!confirm(`Are you sure you want to discharge patient ${patientId}? This cannot be undone.`)) {
    return;
  }
  
  let patients = loadPatients();
  patients = patients.filter((p) => p.id !== patientId);
  savePatients(patients);
  renderPatientTable('');
  alert(`Patient ${patientId} discharged.`);
};

// --- UTILITY FUNCTIONS ---

const generatePatientId = (patients) => {
  if (patients.length === 0) return 'P00001';
  
  // Find the highest number and increment it
  const lastId = patients[patients.length - 1].id;
  const lastNumber = parseInt(lastId.replace('P', ''), 10);
  const newNumber = lastNumber + 1;
  return 'P' + String(newNumber).padStart(5, '0');
};

const resetPatientForm = () => {
  document.getElementById('patientForm').reset();
  document.getElementById('patientId').value = '';
  document.getElementById('formTitle').textContent = 'Add New Patient Record';
  document.getElementById('formTitle').classList.remove('edit-form-heading');
  document.getElementById('savePatientBtn').textContent = 'Save New Record';
  document.getElementById('cancelEditBtn').style.display = 'none';
};

const populateFormForEdit = (patientId) => {
  const userPerms = getCurrentPermissions();
  if (!userPerms.canEdit) {
    alert('Permission Denied: You cannot open the form for editing.');
    return;
  }
  
  const patients = loadPatients();
  const patient = patients.find((p) => p.id === patientId);
  if (!patient) return;

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
};

// Function to control the "Add New Patient" tab visibility
const updateUIToReflectRole = () => {
    const userPerms = getCurrentPermissions();
    const addTab = document.getElementById('add-tab').parentElement; // The list item containing the tab

    if (userPerms.canAdd || userPerms.canEdit) {
        addTab.style.display = 'block'; // Show if they can add or edit
    } else {
        addTab.style.display = 'none'; // Hide if only viewing
    }
    
    // Important: Re-render the table to correctly show/hide action buttons
    renderPatientTable(''); 
};


// --- EVENT LISTENERS (The glue) ---

document.addEventListener('DOMContentLoaded', () => {
  
  // Check login state on load
  const loggedInUser = sessionStorage.getItem('hms_user');
  const loggedInRole = sessionStorage.getItem('hms_role');
  if (loggedInUser && loggedInRole) {
    document.getElementById('loggedInUser').textContent = `${loggedInRole} (${loggedInUser})`;
    document.getElementById('login-view').style.display = 'none';
    document.getElementById('dashboard-view').style.display = 'block';
    updateUIToReflectRole(); // Apply permissions immediately
  }

  // 1. Login Handler
  document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const userId = document.getElementById('userId').value;
    const password = document.getElementById('password').value;
    
    const user = userRoles[userId];

    if (user && user.password === password) { 
      // Successful login: Store user ID and ROLE in session storage
      sessionStorage.setItem('hms_user', userId);
      sessionStorage.setItem('hms_role', user.role);
      
      document.getElementById('loggedInUser').textContent = `${user.role} (${userId})`;
      document.getElementById('login-view').style.display = 'none';
      document.getElementById('dashboard-view').style.display = 'block';
      
      updateUIToReflectRole(); // Apply permissions
    } else {
      alert('Invalid User ID or Password. Try admin/1234, doctor/pass, or user/view.');
    }
  });

  // 2. Logout Handler
  document.getElementById('logoutBtn').addEventListener('click', () => {
    sessionStorage.removeItem('hms_user');
    sessionStorage.removeItem('hms_role');
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
    renderPatientTable(query);
  });
});