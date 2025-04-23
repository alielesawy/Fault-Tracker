document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Enable Bootstrap form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Date picker initialization for date inputs
    var dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Make sure we have a valid date format for the input
        input.addEventListener('change', function() {
            const date = new Date(this.value);
            if (isNaN(date.getTime())) {
                this.setCustomValidity('Please enter a valid date');
            } else {
                this.setCustomValidity('');
            }
        });
    });
    
    // Date range pickers for report generation
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (startDateInput && endDateInput) {
        startDateInput.addEventListener('change', function() {
            // Set the min date of end date to be the start date
            endDateInput.min = this.value;
            
            // If end date is before start date, reset it
            if (endDateInput.value && endDateInput.value < this.value) {
                endDateInput.value = this.value;
            }
        });
        
        endDateInput.addEventListener('change', function() {
            // Set the max date of start date to be the end date
            startDateInput.max = this.value;
            
            // If start date is after end date, reset it
            if (startDateInput.value && startDateInput.value > this.value) {
                startDateInput.value = this.value;
            }
        });
    }
    
    // Confirmation dialog for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
    
    // Filter functionality for tables
    const tableFilter = document.getElementById('tableFilter');
    if (tableFilter) {
        tableFilter.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const table = document.querySelector(this.dataset.table);
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filterValue) ? '' : 'none';
            });
        });
    }
    
    // Dynamic form fields for device selection based on unit
    const unitSelect = document.getElementById('unit_id');
    const deviceNameInput = document.getElementById('device_name');
    const serialNumberInput = document.getElementById('serial_number');
    
    if (unitSelect && deviceNameInput) {
        unitSelect.addEventListener('change', function() {
            // If we have a device selection dropdown, update it based on the selected unit
            const deviceSelect = document.getElementById('device_id');
            if (deviceSelect) {
                // This would typically be an AJAX call to get devices for the selected unit
                // For simplicity, we're just resetting the field here
                deviceSelect.innerHTML = '<option value="">Select a device</option>';
            }
            
            // Reset device name and serial number
            if (deviceNameInput) deviceNameInput.value = '';
            if (serialNumberInput) serialNumberInput.value = '';
        });
    }
    
    // Auto-populate device details when a device is selected
    const deviceSelect = document.getElementById('device_id');
    if (deviceSelect) {
        deviceSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.value) {
                // Typically would fetch device details via AJAX
                // For simplicity, using data attributes on the option
                if (deviceNameInput) deviceNameInput.value = selectedOption.dataset.name || '';
                if (serialNumberInput) serialNumberInput.value = selectedOption.dataset.serial || '';
            } else {
                // Reset fields if no device is selected
                if (deviceNameInput) deviceNameInput.value = '';
                if (serialNumberInput) serialNumberInput.value = '';
            }
        });
    }
});
