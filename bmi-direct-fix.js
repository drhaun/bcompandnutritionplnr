/**
 * Direct BMI calculation fix to ensure the BMI value displays in the field
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log("BMI Direct Fix: Initializing");

  // Find key elements
  const weightKgField = document.getElementById('weight-kg-final');
  const heightCmField = document.getElementById('height-cm');
  const bmiResultField = document.getElementById('bmi-result');
  const bmiCategoryText = document.getElementById('bmi-category');
  
  if (weightKgField && heightCmField && bmiResultField) {
    console.log("BMI Direct Fix: Found all required fields");
    
    // Function to calculate and display BMI
    function calculateAndDisplayBMI() {
      const weightKg = parseFloat(weightKgField.value) || 0;
      const heightCm = parseFloat(heightCmField.value) || 0;
      
      if (weightKg > 0 && heightCm > 0) {
        // Calculate BMI - weight(kg) / height(m)²
        const heightM = heightCm / 100;
        const bmi = weightKg / (heightM * heightM);
        const bmiRounded = Math.round(bmi * 10) / 10; // Round to 1 decimal place
        
        // Set the BMI result value directly
        bmiResultField.value = bmiRounded;
        console.log("BMI Direct Fix: Set BMI value to", bmiRounded);
        
        // Update BMI category if element exists
        if (bmiCategoryText) {
          let category = '';
          if (bmi < 18.5) category = 'Underweight';
          else if (bmi < 25) category = 'Normal weight';
          else if (bmi < 30) category = 'Overweight';
          else if (bmi < 35) category = 'Obesity Class I';
          else if (bmi < 40) category = 'Obesity Class II';
          else category = 'Obesity Class III';
          
          bmiCategoryText.textContent = 'Category: ' + category;
          console.log("BMI Direct Fix: Updated category to", category);
        }
      }
    }
    
    // Add event listeners to weight and height fields
    weightKgField.addEventListener('input', calculateAndDisplayBMI);
    heightCmField.addEventListener('input', calculateAndDisplayBMI);
    
    // Also listen for changes to the weight in pounds field, which may update kg
    const weightLbsField = document.getElementById('weight-lbs-final');
    if (weightLbsField) {
      weightLbsField.addEventListener('input', calculateAndDisplayBMI);
    }
    
    // Run calculation once at startup to handle pre-filled values
    calculateAndDisplayBMI();
    
    // Set a timer to run it again after a short delay 
    // This handles cases where fields are populated by other scripts
    setTimeout(calculateAndDisplayBMI, 500);
  } else {
    console.log("BMI Direct Fix: Could not find required fields", {
      weightKg: !!weightKgField,
      heightCm: !!heightCmField,
      bmiResult: !!bmiResultField
    });
  }
});