/**
 * Better CSV Viewer
 * Shows all columns from CSV files in a clean, scrollable table with visible headers
 */

document.addEventListener('DOMContentLoaded', function() {
  // Set up file input handlers - directly attach to file inputs
  const scanFileInput = document.getElementById('scan-csv-file-input');
  if (scanFileInput) {
    scanFileInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        console.log("File selected via input:", file.name);
        console.log("Processing scan file:", file.name);
        handleScanFile(file);
      }
    });
  }
  
  const usFileInput = document.getElementById('us-csv-file-input');
  if (usFileInput) {
    usFileInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        console.log("File selected via input:", file.name);
        console.log("Processing ultrasound file:", file.name);
        handleUltrasoundFile(file);
      }
    });
  }
});

// Process 3D scan file
function handleScanFile(file) {
  if (!file || !file.name.endsWith('.csv')) {
    alert('Please select a CSV file');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    Papa.parse(e.target.result, {
      header: true,
      skipEmptyLines: true,
      complete: function(results) {
        console.log("Successfully parsed scan CSV with " + results.data.length + " records");
        if (results.data.length > 0) {
          displayBetterScanTable(results.data);
        } else {
          alert('No data found in CSV file');
        }
      },
      error: function(error) {
        alert('Error parsing CSV: ' + error.message);
      }
    });
  };
  reader.readAsText(file);
}

// Process ultrasound file
function handleUltrasoundFile(file) {
  if (!file || !file.name.endsWith('.csv')) {
    alert('Please select a CSV file');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    Papa.parse(e.target.result, {
      header: true,
      skipEmptyLines: true,
      complete: function(results) {
        displayBetterUltrasoundTable(results.data);
      },
      error: function(error) {
        alert('Error parsing CSV: ' + error.message);
      }
    });
  };
  reader.readAsText(file);
}

// Display scan data in a proper table with all columns
function displayBetterScanTable(records) {
  const container = document.querySelector('.scan-measurements-section');
  if (!container) {
    console.error("Scan measurements section not found");
    return;
  }
  
  // Clear previous content
  container.innerHTML = '';
  
  // Create header
  const header = document.createElement('h5');
  header.className = 'mb-3 text-primary';
  header.innerHTML = `<i class="bi bi-table me-2"></i>3D Scan Records (${records.length})`;
  container.appendChild(header);
  
  // Create scrollable container
  const tableContainer = document.createElement('div');
  tableContainer.style.maxHeight = '400px';
  tableContainer.style.overflowY = 'auto';
  tableContainer.style.overflowX = 'auto';
  tableContainer.style.border = '1px solid #dee2e6';
  tableContainer.style.marginBottom = '20px';
  container.appendChild(tableContainer);
  
  // Create table
  const table = document.createElement('table');
  table.className = 'table table-sm table-striped table-bordered';
  table.style.marginBottom = '0';
  tableContainer.appendChild(table);
  
  // Get all columns (excluding empty keys)
  const allColumns = Object.keys(records[0]).filter(key => key !== '');
  
  // Create table header
  const thead = document.createElement('thead');
  table.appendChild(thead);
  
  const headerRow = document.createElement('tr');
  thead.appendChild(headerRow);
  
  // Add columns to header
  allColumns.forEach(column => {
    const th = document.createElement('th');
    th.textContent = column;
    th.style.position = 'sticky';
    th.style.top = '0';
    th.style.backgroundColor = '#f8f9fa';
    th.style.color = '#000';
    th.style.borderBottom = '2px solid #dee2e6';
    th.style.padding = '8px';
    th.style.whiteSpace = 'nowrap';
    headerRow.appendChild(th);
  });
  
  // Add action column header
  const actionTh = document.createElement('th');
  actionTh.textContent = 'Action';
  actionTh.style.position = 'sticky';
  actionTh.style.top = '0';
  actionTh.style.backgroundColor = '#f8f9fa';
  actionTh.style.color = '#000';
  actionTh.style.borderBottom = '2px solid #dee2e6';
  actionTh.style.padding = '8px';
  actionTh.style.textAlign = 'center';
  actionTh.style.whiteSpace = 'nowrap';
  headerRow.appendChild(actionTh);
  
  // Create table body
  const tbody = document.createElement('tbody');
  table.appendChild(tbody);
  
  // Add data rows
  records.forEach(record => {
    const row = document.createElement('tr');
    
    // Add data cells
    allColumns.forEach(column => {
      const td = document.createElement('td');
      td.textContent = record[column] || '';
      row.appendChild(td);
    });
    
    // Add action cell
    const actionTd = document.createElement('td');
    actionTd.style.textAlign = 'center';
    
    const useButton = document.createElement('button');
    useButton.className = 'btn btn-primary btn-sm';
    useButton.textContent = 'Use';
    useButton.onclick = function() {
      useScanRecord(record);
    };
    
    actionTd.appendChild(useButton);
    row.appendChild(actionTd);
    
    tbody.appendChild(row);
  });
}

// Display ultrasound data in a proper table with all columns
function displayBetterUltrasoundTable(records) {
  const container = document.querySelector('.us-measurements-section');
  if (!container) {
    console.error("Ultrasound measurements section not found");
    return;
  }
  
  // Clear previous content
  container.innerHTML = '';
  
  // Create header
  const header = document.createElement('h5');
  header.className = 'mb-3 text-primary';
  header.innerHTML = `<i class="bi bi-table me-2"></i>Ultrasound Records (${records.length})`;
  container.appendChild(header);
  
  // Create scrollable container
  const tableContainer = document.createElement('div');
  tableContainer.style.maxHeight = '400px';
  tableContainer.style.overflowY = 'auto';
  tableContainer.style.overflowX = 'auto';
  tableContainer.style.border = '1px solid #dee2e6';
  tableContainer.style.marginBottom = '20px';
  container.appendChild(tableContainer);
  
  // Create table
  const table = document.createElement('table');
  table.className = 'table table-sm table-striped table-bordered';
  table.style.marginBottom = '0';
  tableContainer.appendChild(table);
  
  // Get all columns (excluding empty keys)
  const allColumns = Object.keys(records[0]).filter(key => key !== '');
  
  // Create table header
  const thead = document.createElement('thead');
  table.appendChild(thead);
  
  const headerRow = document.createElement('tr');
  thead.appendChild(headerRow);
  
  // Add columns to header
  allColumns.forEach(column => {
    const th = document.createElement('th');
    th.textContent = column;
    th.style.position = 'sticky';
    th.style.top = '0';
    th.style.backgroundColor = '#f8f9fa';
    th.style.color = '#000';
    th.style.borderBottom = '2px solid #dee2e6';
    th.style.padding = '8px';
    th.style.whiteSpace = 'nowrap';
    headerRow.appendChild(th);
  });
  
  // Add action column header
  const actionTh = document.createElement('th');
  actionTh.textContent = 'Action';
  actionTh.style.position = 'sticky';
  actionTh.style.top = '0';
  actionTh.style.backgroundColor = '#f8f9fa';
  actionTh.style.color = '#000';
  actionTh.style.borderBottom = '2px solid #dee2e6';
  actionTh.style.padding = '8px';
  actionTh.style.textAlign = 'center';
  actionTh.style.whiteSpace = 'nowrap';
  headerRow.appendChild(actionTh);
  
  // Create table body
  const tbody = document.createElement('tbody');
  table.appendChild(tbody);
  
  // Add data rows
  records.forEach(record => {
    const row = document.createElement('tr');
    
    // Add data cells
    allColumns.forEach(column => {
      const td = document.createElement('td');
      td.textContent = record[column] || '';
      row.appendChild(td);
    });
    
    // Add action cell
    const actionTd = document.createElement('td');
    actionTd.style.textAlign = 'center';
    
    const useButton = document.createElement('button');
    useButton.className = 'btn btn-primary btn-sm';
    useButton.textContent = 'Use';
    useButton.onclick = function() {
      useUltrasoundRecord(record);
    };
    
    actionTd.appendChild(useButton);
    row.appendChild(actionTd);
    
    tbody.appendChild(row);
  });
}