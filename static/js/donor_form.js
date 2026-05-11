document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('donor-registration-form');
  
  if (!form) return;

  const inputs = {
    fullName: form.querySelector('input[name="full_name"]'),
    email: form.querySelector('input[name="email"]'),
    phone: form.querySelector('input[name="phone"]'),
    dateOfBirth: form.querySelector('input[name="date_of_birth"]'),
    bloodType: form.querySelector('select[name="blood_type"]'),
    city: form.querySelector('input[name="city"]'),
    healthConfirm: form.querySelector('input[name="health_confirm"]'),
    submitBtn: form.querySelector('button[type="submit"]')
  };

  const validationRules = {
    full_name: {
      element: inputs.fullName,
      validate: (value) => value.trim().length >= 3,
      message: 'Full name must be at least 3 characters'
    },
    email: {
      element: inputs.email,
      validate: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
      message: 'Please enter a valid email address'
    },
    phone: {
      element: inputs.phone,
      validate: (value) => {
        const digits = value.replace(/\D/g, '');
        return digits.length >= 8;
      },
      message: 'Please enter a valid phone number'
    },
    date_of_birth: {
      element: inputs.dateOfBirth,
      validate: (value) => {
        if (!value) return false;
        const birthDate = new Date(value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        return age >= 18;
      },
      message: 'You must be at least 18 years old to donate'
    },
    blood_type: {
      element: inputs.bloodType,
      validate: (value) => value !== '',
      message: 'Please select your blood type'
    },
    city: {
      element: inputs.city,
      validate: (value) => value.trim() !== '',
      message: 'Please enter your city'
    },
    health_confirm: {
      element: inputs.healthConfirm,
      validate: (value, element) => element.checked,
      message: 'You must confirm you are in good health'
    }
  };

  function showError(input, message) {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    
    let feedback = input.nextElementSibling;
    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
      feedback = document.createElement('div');
      feedback.className = 'invalid-feedback';
      input.parentNode.appendChild(feedback);
    }
    feedback.textContent = message;
    feedback.style.display = 'block';
  }

  function clearError(input) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
    
    let feedback = input.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
      feedback.textContent = '';
      feedback.style.display = 'none';
    }
  }

  function validateField(fieldName) {
    const rule = validationRules[fieldName];
    if (!rule || !rule.element) return true;

    const value = rule.element.type === 'checkbox' 
      ? rule.element.checked 
      : rule.element.value;
    
    const isValid = rule.validate(value, rule.element);
    
    if (isValid) {
      clearError(rule.element);
    } else {
      showError(rule.element, rule.message);
    }
    
    return isValid;
  }

  function countValidFields() {
    let validCount = 0;
    for (const fieldName in validationRules) {
      const rule = validationRules[fieldName];
      if (!rule.element) continue;
      
      const value = rule.element.type === 'checkbox'
        ? rule.element.checked
        : rule.element.value;
      
      if (rule.validate(value, rule.element)) {
        validCount++;
      }
    }
    return validCount;
  }

  function updateProgressBar() {
    const validCount = countValidFields();
    const totalFields = Object.keys(validationRules).length;
    const percentage = (validCount / totalFields) * 100;
    
    let progressContainer = document.getElementById('donor-form-progress');
    if (!progressContainer) {
      progressContainer = document.createElement('div');
      progressContainer.id = 'donor-form-progress';
      progressContainer.className = 'progress mb-3';
      progressContainer.style.height = '6px';
      
      const progressBar = document.createElement('div');
      progressBar.id = 'donor-form-progress-bar';
      progressBar.className = 'progress-bar bg-success';
      progressBar.style.width = '0%';
      progressBar.style.transition = 'width 0.3s ease';
      
      progressContainer.appendChild(progressBar);
      form.insertBefore(progressContainer, inputs.submitBtn);
    }
    
    const progressBar = document.getElementById('donor-form-progress-bar');
    progressBar.style.width = percentage + '%';
  }

  for (const fieldName in validationRules) {
    const rule = validationRules[fieldName];
    if (!rule.element) continue;
    
    rule.element.addEventListener('input', function() {
      validateField(fieldName);
      updateProgressBar();
    });
    
    rule.element.addEventListener('change', function() {
      validateField(fieldName);
      updateProgressBar();
    });
  }

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    let firstInvalidField = null;
    let allValid = true;
    
    for (const fieldName in validationRules) {
      const isValid = validateField(fieldName);
      if (!isValid) {
        allValid = false;
        if (!firstInvalidField) {
          firstInvalidField = validationRules[fieldName].element;
        }
      }
    }
    
    if (!allValid) {
      if (firstInvalidField) {
        firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstInvalidField.focus();
      }
      return;
    }
    
    inputs.submitBtn.textContent = 'Registering...';
    inputs.submitBtn.disabled = true;
    
    form.submit();
  });

  updateProgressBar();
});
