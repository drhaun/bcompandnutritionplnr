/**
 * BMI Calculator
 * Calculates BMI based on weight and height
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log("Initializing BMI Calculator");
  
  // Get weight and height input elements
  const weightKgInput = document.getElementById('weight-kg-final');
  const heightCmInput = document.getElementById('height-cm');
  const confirmWeightBtn = document.getElementById('confirm-weight-btn');
  
  // Set up event listeners for changes to weight or height
  if (weightKgInput && heightCmInput) {
    weightKgInput.addEventListener('input', calculateBMI);
    heightCmInput.addEventListener('input', calculateBMI);
    console.log("Added input listeners to weight and height fields for BMI calculation");
  }
  
  // Add event listener to the confirm weight button
  if (confirmWeightBtn) {
    confirmWeightBtn.addEventListener('click', calculateBMI);
    console.log("Added click listener to confirm weight button for BMI calculation");
  }
  
  // Add event listeners to all weight input fields
  const weightInputs = document.querySelectorAll('input[id^="weight-"]');
  weightInputs.forEach(input => {
    input.addEventListener('input', function() {
      // When any weight field changes, update the BMI
      setTimeout(calculateBMI, 100); // Small delay to ensure values are updated
    });
  });
  
  // Initial calculation if there are already values
  calculateBMI();
});

/**
 * Calculate BMI based on weight and height
 */
function calculateBMI() {
  console.log("Running BMI calculation");
  const weightKgInput = document.getElementById('weight-kg-final');
  const heightCmInput = document.getElementById('height-cm');
  const bmiResult = document.getElementById('bmi-result');
  const bmiCategory = document.getElementById('bmi-category');
  
  console.log("Found elements: weightKg:", !!weightKgInput, "heightCm:", !!heightCmInput, "bmiResult:", !!bmiResult, "bmiCategory:", !!bmiCategory);
  
  if (!weightKgInput || !heightCmInput || !bmiResult || !bmiCategory) {
    console.log("Missing required elements for BMI calculation");
    return;
  }
  
  // Get weight and height values
  let weightKg = parseFloat(weightKgInput.value);
  // If final weight is not set, try to get it from other fields
  if (isNaN(weightKg) || weightKg <= 0) {
    const weightKgAlt = document.getElementById('weight-kg');
    if (weightKgAlt && !isNaN(parseFloat(weightKgAlt.value)) && parseFloat(weightKgAlt.value) > 0) {
      weightKg = parseFloat(weightKgAlt.value);
      // Auto-update the final weight field
      weightKgInput.value = weightKg;
    }
  }
  const heightCm = parseFloat(heightCmInput.value);
  
  // Check if values are valid
  if (isNaN(weightKg) || isNaN(heightCm) || weightKg <= 0 || heightCm <= 0) {
    bmiResult.value = '';
    bmiCategory.textContent = 'Category: --';
    return;
  }
  
  // Convert height to meters and calculate BMI
  const heightM = heightCm / 100;
  const bmi = weightKg / (heightM * heightM);
  
  // Update BMI result
  bmiResult.value = bmi.toFixed(1);
  console.log("Set BMI result value to:", bmi.toFixed(1));
  
  // Determine BMI category
  let category = '';
  let categoryClass = '';
  
  if (bmi < 18.5) {
    category = 'Underweight';
    categoryClass = 'text-warning';
  } else if (bmi < 25) {
    category = 'Normal weight';
    categoryClass = 'text-success';
  } else if (bmi < 30) {
    category = 'Overweight';
    categoryClass = 'text-warning';
  } else if (bmi < 35) {
    category = 'Obesity Class I';
    categoryClass = 'text-danger';
  } else if (bmi < 40) {
    category = 'Obesity Class II';
    categoryClass = 'text-danger';
  } else {
    category = 'Obesity Class III';
    categoryClass = 'text-danger';
  }
  
  // Update BMI category
  bmiCategory.textContent = `Category: ${category}`;
  bmiCategory.className = `form-text mt-1 ${categoryClass}`;
  
  console.log("Calculated BMI:", bmi.toFixed(1), "Category:", category);
  
  // Also update hidden field for report if it exists
  const bmiTable = document.getElementById('bmi-table');
  if (bmiTable) {
    bmiTable.textContent = bmi.toFixed(1);
  }
  
  const bmiCategoryTable = document.getElementById('bmi-category-table');
  if (bmiCategoryTable) {
    bmiCategoryTable.textContent = category;
  }
}