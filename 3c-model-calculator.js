/**
 * 3C-Model Calculator
 * Handles calculation of body composition using the 3-Component Model
 * (Body Density + Total Body Water)
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log("Initializing 3C-Model Calculator");
  
  // Set up 3C-Model calculation button
  const calcModelBtn = document.getElementById('calculate-3c-model-btn');
  if (calcModelBtn) {
    calcModelBtn.addEventListener('click', function() {
      calculate3CModel();
    });
    console.log("Added click handler to 3C-Model button");
  }
  
  // Set up site selection change handlers
  const sitesCountSelect = document.getElementById('sites-count');
  const genderSelect = document.getElementById('gender');
  const genderSpecificCheckbox = document.getElementById('use-gender-specific');
  
  if (sitesCountSelect) {
    sitesCountSelect.addEventListener('change', function() {
      updateSiteInfo();
    });
  }
  
  if (genderSelect) {
    genderSelect.addEventListener('change', function() {
      updateSiteInfo();
    });
  }
  
  if (genderSpecificCheckbox) {
    genderSpecificCheckbox.addEventListener('change', function() {
      updateSiteInfo();
    });
  }
  
  // Initialize the site selection
  setTimeout(function() {
    updateSiteInfo();
  }, 500);
});

/**
 * Calculate body composition using the 3C-Model formula
 * 3C-Model: BF% = (2.118/BD - 0.78*TBW/100 - 1.354) * 100
 * Where BD is body density and TBW is total body water percentage
 */
function calculate3CModel() {
  console.log("Calculating 3C-Model Body Composition");
  
  try {
    // Get critical values
    const weightLbs = parseFloat(document.getElementById('weight-lbs1').textContent || 0);
    const weightKg = weightLbs * 0.453592;
    
    // Get body density from thickness calculation
    const bodyDensity = parseFloat(document.getElementById('body-density').textContent || 0);
    
    // Get total body water percentage
    const tbwPercent = parseFloat(document.getElementById('ultrasound-water-percent').textContent || 0);
    
    // Get body fat percentages from different methods
    const bodyFatScan = parseFloat(document.getElementById('scan-body-fat').textContent || 0);
    const bodyFatUS = parseFloat(document.getElementById('ultrasound-body-fat').textContent || 0);
    
    // Check if we have sufficient data
    if (weightKg <= 0) {
      alert("Missing weight data. Please enter client weight.");
      return;
    }
    
    if (bodyDensity <= 0) {
      alert("Missing body density. Please calculate thickness values first.");
      return;
    }
    
    if (tbwPercent <= 0) {
      alert("Missing body water percentage. Please enter total body water percentage.");
      return;
    }
    
    console.log("3C-Model inputs:", {
      weightKg: weightKg,
      bodyDensity: bodyDensity,
      tbwPercent: tbwPercent,
      bodyFatScan: bodyFatScan,
      bodyFatUS: bodyFatUS
    });
    
    // Calculate 3C-Model body fat percentage
    // BF% = (2.118/BD - 0.78*TBW/100 - 1.354) * 100
    const bodyFat3C = (2.118 / bodyDensity - 0.78 * tbwPercent / 100 - 1.354) * 100;
    console.log("3C-Model body fat percentage:", bodyFat3C.toFixed(1) + "%");
    
    // Calculate fat mass and fat-free mass based on 3C-Model
    const fatMassKg = weightKg * (bodyFat3C / 100);
    const fatMassLbs = fatMassKg * 2.20462;
    const ffmKg = weightKg - fatMassKg;
    const ffmLbs = ffmKg * 2.20462;
    
    // Update the final results table
    document.getElementById('display-3c-model-body-fat').textContent = bodyFat3C.toFixed(1);
    document.getElementById('3c-model-fat-mass-kg').textContent = fatMassKg.toFixed(1);
    document.getElementById('3c-model-fat-mass-lbs').textContent = fatMassLbs.toFixed(1);
    document.getElementById('3c-model-ffm-kg').textContent = ffmKg.toFixed(1);
    document.getElementById('3c-model-ffm-lbs').textContent = ffmLbs.toFixed(1);
    
    // Update scan values in the table if available
    if (bodyFatScan > 0) {
      const scanFatMassKg = weightKg * (bodyFatScan / 100);
      const scanFatMassLbs = scanFatMassKg * 2.20462;
      const scanFfmKg = weightKg - scanFatMassKg;
      const scanFfmLbs = scanFfmKg * 2.20462;
      
      document.getElementById('display-scan-body-fat').textContent = bodyFatScan.toFixed(1);
      document.getElementById('scan-fat-mass-kg').textContent = scanFatMassKg.toFixed(1);
      document.getElementById('scan-fat-mass-lbs').textContent = scanFatMassLbs.toFixed(1);
      document.getElementById('scan-ffm-kg').textContent = scanFfmKg.toFixed(1);
      document.getElementById('scan-ffm-lbs').textContent = scanFfmLbs.toFixed(1);
    }
    
    // Update ultrasound values in the table if available
    if (bodyFatUS > 0) {
      const usFatMassKg = weightKg * (bodyFatUS / 100);
      const usFatMassLbs = usFatMassKg * 2.20462;
      const usFfmKg = weightKg - usFatMassKg;
      const usFfmLbs = usFfmKg * 2.20462;
      
      document.getElementById('display-ultrasound-body-fat').textContent = bodyFatUS.toFixed(1);
      document.getElementById('ultrasound-fat-mass-kg').textContent = usFatMassKg.toFixed(1);
      document.getElementById('ultrasound-fat-mass-lbs').textContent = usFatMassLbs.toFixed(1);
      document.getElementById('ultrasound-ffm-kg').textContent = usFfmKg.toFixed(1);
      document.getElementById('ultrasound-ffm-lbs').textContent = usFfmLbs.toFixed(1);
    }
    
    // Calculate average body fat percentage
    const methods = [];
    if (bodyFat3C > 0) methods.push(bodyFat3C);
    if (bodyFatScan > 0) methods.push(bodyFatScan);
    if (bodyFatUS > 0) methods.push(bodyFatUS);
    
    if (methods.length > 0) {
      const avgBodyFat = methods.reduce((sum, val) => sum + val, 0) / methods.length;
      const avgFatMassKg = weightKg * (avgBodyFat / 100);
      const avgFatMassLbs = avgFatMassKg * 2.20462;
      const avgFfmKg = weightKg - avgFatMassKg;
      const avgFfmLbs = avgFfmKg * 2.20462;
      
      document.getElementById('display-average-body-fat').textContent = avgBodyFat.toFixed(1);
      document.getElementById('average-fat-mass-kg').textContent = avgFatMassKg.toFixed(1);
      document.getElementById('average-fat-mass-lbs').textContent = avgFatMassLbs.toFixed(1);
      document.getElementById('average-ffm-kg').textContent = avgFfmKg.toFixed(1);
      document.getElementById('average-ffm-lbs').textContent = avgFfmLbs.toFixed(1);
    }
    
    // Show the final results section
    const finalResultsSection = document.querySelector('.final-body-composition-results');
    if (finalResultsSection) {
      finalResultsSection.style.display = 'block';
    }
    
    // Scroll to the final results
    finalResultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    return bodyFat3C;
  } catch (err) {
    console.error("Error calculating 3C-Model:", err);
    alert("Error calculating 3C-Model. Please check your data and try again.");
    return null;
  }
}

/**
 * Update the site info text and show/hide relevant input fields
 * based on the selected measurement protocol
 */
function updateSiteInfo() {
  const sitesCount = document.getElementById('sites-count').value;
  const siteInfoText = document.getElementById('site-info-text');
  const isGenderSpecific = document.getElementById('use-gender-specific')?.checked || true;
  const gender = document.getElementById('gender')?.value || 'male';
  
  let infoText = '';
  
  if (sitesCount === '3') {
    if (isGenderSpecific) {
      if (gender === 'male') {
        infoText = '<span class="badge bg-primary">3-Site (Male):</span> Chest, Abdomen, Thigh';
      } else {
        infoText = '<span class="badge bg-primary">3-Site (Female):</span> Tricep, Suprailiac, Thigh';
      }
    } else {
      infoText = '<span class="badge bg-primary">3-Site:</span> Chest, Abdomen, Thigh';
    }
  } else if (sitesCount === '4') {
    infoText = '<span class="badge bg-primary">4-Site:</span> Abdomen, Thigh, Tricep, Subscapular';
  } else if (sitesCount === '7') {
    infoText = '<span class="badge bg-primary">7-Site:</span> Chest, Abdomen, Thigh, Tricep, Subscapular, Axilla, Hip (most accurate)';
  }
  
  if (siteInfoText) {
    siteInfoText.innerHTML = infoText;
  }
  
  // Show/hide relevant input fields based on selected method
  const allSites = ['chest', 'abdomen', 'thigh', 'tricep', 'subscapular', 'axilla', 'hip'];
  let visibleSites = [];
  
  if (sitesCount === '3') {
    if (isGenderSpecific && gender === 'female') {
      visibleSites = ['tricep', 'hip', 'thigh']; // Using hip as suprailiac
    } else {
      visibleSites = ['chest', 'abdomen', 'thigh'];
    }
  } else if (sitesCount === '4') {
    visibleSites = ['abdomen', 'thigh', 'tricep', 'subscapular'];
  } else if (sitesCount === '7') {
    visibleSites = allSites;
  }
  
  // Show/hide rows based on selected method
  allSites.forEach(site => {
    const row = document.getElementById(site + '-thickness-row');
    if (row) {
      if (visibleSites.includes(site)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  });
  
  console.log(`Updated site info for ${sitesCount}-site method, gender-specific: ${isGenderSpecific}`);
}