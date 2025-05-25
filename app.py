from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, send_file
import os
import logging
from datetime import datetime
from models import db, Client, RmrData, BodyCompositionData, UltrasoundData
import csv
import io
import numpy as np
from sqlalchemy import func
from app_routes import generate_pdf_report

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///rmr_data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/body-composition')
def body_composition():
    """Serve the body composition page as the main page."""
    return render_template('direct_entry.html')
    
@app.route('/report')
def report():
    """Serve a simple HTML report page with all form data directly passed to the template."""
    from datetime import datetime
    
    # Get form data from query parameters
    name = request.args.get('name', 'No Name')
    age = request.args.get('age', 'N/A')
    gender = request.args.get('gender', 'N/A')
    email = request.args.get('email', 'N/A')
    height_in = request.args.get('height_in', 'N/A')
    height_cm = request.args.get('height_cm', 'N/A')
    weight_lbs = request.args.get('weight_lbs', 'N/A')
    weight_kg = request.args.get('weight_kg', 'N/A')
    body_fat_percent = request.args.get('body_fat_percent', 'N/A')
    fat_mass_kg = request.args.get('fat_mass_kg', 'N/A')
    fat_mass_lbs = request.args.get('fat_mass_lbs', 'N/A')
    ffm_kg = request.args.get('ffm_kg', 'N/A')
    ffm_lbs = request.args.get('ffm_lbs', 'N/A')
    
    # Pass all values directly to the template
    return render_template('simplest_report.html', 
                          current_date=datetime.now().strftime('%Y-%m-%d'),
                          name=name,
                          age=age,
                          gender=gender,
                          email=email,
                          height_in=height_in,
                          height_cm=height_cm,
                          weight_lbs=weight_lbs,
                          weight_kg=weight_kg,
                          body_fat_percent=body_fat_percent,
                          fat_mass_kg=fat_mass_kg,
                          fat_mass_lbs=fat_mass_lbs,
                          ffm_kg=ffm_kg,
                          ffm_lbs=ffm_lbs)
    


# Simplified app - only body composition page needed

@app.route('/direct-report')
def direct_report():
    """Display a simple form with live report preview."""
    return render_template('direct_report.html')
    
@app.route('/basic-report')
def basic_report():
    """Generate a basic report from query parameters."""
    # Get all form data from query parameters
    name = request.args.get('name', 'N/A')
    email = request.args.get('email', 'N/A')
    gender = request.args.get('gender', 'Male')
    age = request.args.get('age', 'N/A')
    assessment_date = request.args.get('assessment_date', 'N/A')
    
    height_in = request.args.get('height_in', 'N/A')
    height_cm = request.args.get('height_cm', 'N/A')
    weight_lbs = request.args.get('weight_lbs', 'N/A')
    weight_kg = request.args.get('weight_kg', 'N/A')
    
    water_device1 = request.args.get('water_device1', '')
    water_percent1 = request.args.get('water_percent1', 'N/A')
    water_liters1 = request.args.get('water_liters1', 'N/A')
    
    water_device2 = request.args.get('water_device2', '')
    water_percent2 = request.args.get('water_percent2', 'N/A')
    water_liters2 = request.args.get('water_liters2', 'N/A')
    
    water_device3 = request.args.get('water_device3', '')
    water_percent3 = request.args.get('water_percent3', 'N/A')
    water_liters3 = request.args.get('water_liters3', 'N/A')
    
    water_liters_avg = request.args.get('water_liters_avg', 'N/A')
    water_liters_final = request.args.get('water_liters_final', 'N/A')
    
    specific_gravity = request.args.get('specific_gravity', 'N/A')
    hydration_status = request.args.get('hydration_status', 'N/A')
    
    body_density = request.args.get('body_density', 'N/A')
    body_fat_percent = request.args.get('body_fat_percent', 'N/A')
    fat_mass_kg = request.args.get('fat_mass_kg', 'N/A')
    fat_mass_lbs = request.args.get('fat_mass_lbs', 'N/A')
    fat_free_mass_kg = request.args.get('fat_free_mass_kg', 'N/A')
    fat_free_mass_lbs = request.args.get('fat_free_mass_lbs', 'N/A')
    
    # Render template with all data
    return render_template('basic_report.html',
                          name=name,
                          email=email,
                          gender=gender,
                          age=age,
                          assessment_date=assessment_date,
                          height_in=height_in,
                          height_cm=height_cm,
                          weight_lbs=weight_lbs,
                          weight_kg=weight_kg,
                          water_device1=water_device1,
                          water_percent1=water_percent1,
                          water_liters1=water_liters1,
                          water_device2=water_device2,
                          water_percent2=water_percent2,
                          water_liters2=water_liters2,
                          water_device3=water_device3,
                          water_percent3=water_percent3,
                          water_liters3=water_liters3,
                          water_liters_avg=water_liters_avg,
                          water_liters_final=water_liters_final,
                          specific_gravity=specific_gravity,
                          hydration_status=hydration_status,
                          body_density=body_density,
                          body_fat_percent=body_fat_percent,
                          fat_mass_kg=fat_mass_kg,
                          fat_mass_lbs=fat_mass_lbs,
                          fat_free_mass_kg=fat_free_mass_kg,
                          fat_free_mass_lbs=fat_free_mass_lbs)
    
@app.route('/simple')
def simple():
    """Display a very simple form with real-time preview."""
    return render_template('simple.html')
    
@app.route('/final')
def final_solution():
    """Display all-in-one form with real-time calculations and report."""
    return render_template('final_solution.html')
    
@app.route('/simple-form')
def simple_form():
    """Display a simple form that will definitely work."""
    return render_template('simple_form.html')
    
@app.route('/generate-report', methods=['POST'])
def generate_report():
    """Generate a report from the simple form data."""
    from datetime import datetime
    
    # Get form data directly from POST request
    name = request.form.get('name', 'No Name')
    age = request.form.get('age', 'N/A')
    gender = request.form.get('gender', 'N/A')
    email = request.form.get('email', 'N/A')
    height_in = request.form.get('height_in', 'N/A')
    height_cm = str(round(float(height_in) * 2.54, 1)) if height_in and height_in != 'N/A' else 'N/A'
    weight_lbs = request.form.get('weight_lbs', 'N/A')
    weight_kg = str(round(float(weight_lbs) * 0.453592, 1)) if weight_lbs and weight_lbs != 'N/A' else 'N/A'
    
    # Pass all values directly to the template
    return render_template('simplest_report.html', 
                          current_date=datetime.now().strftime('%Y-%m-%d'),
                          name=name,
                          age=age,
                          gender=gender,
                          email=email,
                          height_in=height_in,
                          height_cm=height_cm,
                          weight_lbs=weight_lbs,
                          weight_kg=weight_kg,
                          body_fat_percent='N/A',
                          fat_mass_kg='N/A',
                          fat_mass_lbs='N/A',
                          ffm_kg='N/A',
                          ffm_lbs='N/A')

@app.route('/save-body-composition', methods=['POST'])
def save_body_composition():
    """Save body composition data."""
    if not request.json:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    try:
        data = request.json
        client_data = data.get('client_data', {})
        scan_data = data.get('scan_data', [])
        ultrasound_data = data.get('ultrasound_data', [])
        
        # Parse test date
        test_date = None
        if client_data.get('test_date'):
            try:
                test_date = datetime.strptime(client_data['test_date'], '%Y-%m-%d').date()
            except ValueError:
                test_date = None
        
        # Create or update client
        client_id = client_data.get('id')
        if client_id:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'status': 'error', 'message': 'Client not found'}), 404
        else:
            client = Client()
        
        # Update client data
        client.first_name = client_data.get('first_name', '')
        client.last_name = client_data.get('last_name', '')
        client.age = int(client_data.get('age', 0)) if client_data.get('age') else None
        client.gender = client_data.get('gender', '')
        client.weight_kg = float(client_data.get('weight_kg', 0)) if client_data.get('weight_kg') else None
        client.weight_lbs = float(client_data.get('weight_lbs', 0)) if client_data.get('weight_lbs') else None
        client.height_cm = float(client_data.get('height_cm', 0)) if client_data.get('height_cm') else None
        client.height_in = float(client_data.get('height_in', 0)) if client_data.get('height_in') else None
        client.test_date = test_date
        
        # Update body composition data
        client.body_fat_percent = float(client_data.get('body_fat_percent', 0)) if client_data.get('body_fat_percent') else None
        client.lean_mass_kg = float(client_data.get('lean_mass_kg', 0)) if client_data.get('lean_mass_kg') else None
        client.lean_mass_lbs = float(client_data.get('lean_mass_lbs', 0)) if client_data.get('lean_mass_lbs') else None
        client.fat_mass_kg = float(client_data.get('fat_mass_kg', 0)) if client_data.get('fat_mass_kg') else None
        client.fat_mass_lbs = float(client_data.get('fat_mass_lbs', 0)) if client_data.get('fat_mass_lbs') else None
        
        # Update water data
        client.water_percent1 = float(client_data.get('water_percent1', 0)) if client_data.get('water_percent1') else None
        client.water_percent2 = float(client_data.get('water_percent2', 0)) if client_data.get('water_percent2') else None
        client.water_percent3 = float(client_data.get('water_percent3', 0)) if client_data.get('water_percent3') else None
        client.water_device1 = client_data.get('water_device1', '')
        client.water_device2 = client_data.get('water_device2', '')
        client.water_device3 = client_data.get('water_device3', '')
        client.water_liters1 = float(client_data.get('water_liters1', 0)) if client_data.get('water_liters1') else None
        client.water_liters2 = float(client_data.get('water_liters2', 0)) if client_data.get('water_liters2') else None
        client.water_liters3 = float(client_data.get('water_liters3', 0)) if client_data.get('water_liters3') else None
        client.water_liters_avg = float(client_data.get('water_liters_avg', 0)) if client_data.get('water_liters_avg') else None
        client.water_liters_final = float(client_data.get('water_liters_final', 0)) if client_data.get('water_liters_final') else None
        client.specific_gravity = float(client_data.get('specific_gravity', 0)) if client_data.get('specific_gravity') else None
        client.scan_device = client_data.get('scan_device', '')
        
        db.session.add(client)
        db.session.commit()
        
        # Save scan data if provided
        if scan_data and len(scan_data) > 0:
            # First, remove any existing data points for this client
            BodyCompositionData.query.filter_by(client_id=client.id).delete()
            
            # Add new scan data points
            for row in scan_data:
                # Try to parse the scan date
                scan_date = None
                if row.get('Scan Date'):
                    try:
                        scan_date = datetime.strptime(row['Scan Date'], '%Y-%m-%d %H:%M:%S').date()
                    except ValueError:
                        try:
                            scan_date = datetime.strptime(row['Scan Date'], '%Y-%m-%d').date()
                        except ValueError:
                            scan_date = None
                
                # Add important measurements as separate records
                important_measurements = [
                    'Height', 'Weight', 'Body Fat Percent', 'Lean Mass', 'Fat Mass',
                    'Waist', 'Hips', 'Chest', 'Thigh Left', 'Thigh Right', 'Biceps Left', 'Biceps Right'
                ]
                
                for measurement in important_measurements:
                    if measurement in row and row[measurement]:
                        try:
                            value = float(row[measurement])
                            measurement_data = BodyCompositionData()
                            measurement_data.client_id = client.id
                            measurement_data.scan_date = scan_date
                            measurement_data.measurement_type = client_data.get('scan_device', 'Fit3D')
                            measurement_data.measurement_name = measurement
                            measurement_data.measurement_value = value
                            measurement_data.measurement_unit = ('in' if measurement in ['Height', 'Waist', 'Hips', 'Chest', 'Thigh Left', 'Thigh Right', 'Biceps Left', 'Biceps Right'] else 
                                               'lbs' if measurement in ['Weight', 'Lean Mass', 'Fat Mass'] else '%')
                            db.session.add(measurement_data)
                        except (ValueError, TypeError):
                            pass
            
            db.session.commit()
        
        # Save ultrasound data if provided
        if ultrasound_data and len(ultrasound_data) > 0:
            # First, remove any existing ultrasound data for this client
            UltrasoundData.query.filter_by(client_id=client.id).delete()
            
            # Add new ultrasound data points
            for row in ultrasound_data:
                # Try to parse the date
                us_date = None
                if row.get('Date'):
                    try:
                        us_date = datetime.strptime(row['Date'], '%Y-%m-%d %H-%M').date()
                    except ValueError:
                        try:
                            us_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                        except ValueError:
                            us_date = None
                
                # Add ultrasound measurements
                ultrasound_sites = ['CH', 'WA', 'TR', 'TH', 'AX', 'SC']
                
                for site in ultrasound_sites:
                    if site in row and row[site]:
                        try:
                            value = float(row[site])
                            site_names = {
                                'CH': 'Chest',
                                'WA': 'Waist',
                                'TR': 'Triceps',
                                'TH': 'Thigh',
                                'AX': 'Axilla',
                                'SC': 'Subscapular'
                            }
                            
                            us_data = UltrasoundData()
                            us_data.client_id = client.id
                            us_data.date = us_date
                            us_data.site_name = site_names.get(site, site)
                            us_data.measurement_value = value
                            db.session.add(us_data)
                        except (ValueError, TypeError):
                            pass
            
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Body composition data saved successfully',
            'client_id': client.id
        })
    
    except Exception as e:
        logger.error(f"Error saving body composition data: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error saving data: {str(e)}'}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

@app.route('/api/process-csv', methods=['POST'])
def process_csv():
    """Multi-step CSV processing for RMR metrics."""
    if not request.json:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    try:
        # Get parameters from request
        step = request.json.get('step', 1)
        csv_data = request.json.get('csvData')
        options = request.json.get('options', {})
        
        if not csv_data:
            return jsonify({'status': 'error', 'message': 'No CSV data provided'}), 400
        
        # Process CSV based on step
        if step == 1:
            # Step 1: Remove row 2 (units row)
            processed_data = remove_units_row(csv_data)
            return jsonify({
                'status': 'success',
                'step': 1,
                'processed_data': processed_data,
                'message': 'Units row removed successfully'
            })
        
        elif step == 2:
            # Step 2: Remove time range (2-3 minutes)
            minutes_to_remove = options.get('minutesToRemove', 0)
            processed_data = remove_time_range(csv_data, minutes_to_remove)
            return jsonify({
                'status': 'success',
                'step': 2,
                'processed_data': processed_data,
                'message': f'First {minutes_to_remove} minutes removed successfully'
            })
        
        elif step == 3:
            # Step 3: Final processing and RMR calculation
            client_data = request.json.get('clientData', {}) or {}
            return calculate_rmr(csv_data, client_data)
        
        else:
            return jsonify({'status': 'error', 'message': 'Invalid processing step'}), 400
    
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error processing CSV: {str(e)}'}), 500

def remove_units_row(csv_data):
    """Remove row 2 (units row) from CSV data."""
    try:
        # Parse CSV
        csv_reader = csv.reader(io.StringIO(csv_data))
        rows = list(csv_reader)
        
        # Debug info on CSV data
        logger.debug(f"CSV parsing - received {len(rows)} rows")
        
        if len(rows) < 3:  # Need header + units + at least one data row
            logger.error(f"CSV has insufficient rows: {len(rows)}")
            return csv_data  # Not enough rows to remove
        
        # Remove row 2 (index 1)
        processed_rows = [rows[0]] + rows[2:]
        logger.debug(f"After removing units row: {len(processed_rows)} rows")
        
        # Convert back to CSV string
        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(processed_rows)
        
        return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error removing units row: {str(e)}")
        raise
        
def remove_time_range(csv_data, minutes_to_remove=3):
    """Remove first X minutes of data."""
    try:
        if minutes_to_remove <= 0:
            return csv_data  # No rows to remove
            
        # Parse CSV
        csv_reader = csv.reader(io.StringIO(csv_data))
        rows = list(csv_reader)
        
        if len(rows) < 2:
            return csv_data  # Not enough rows
            
        # Find time column
        header_row = rows[0]
        time_col_idx = -1
        
        for i, header in enumerate(header_row):
            if header.lower() == 'time':
                time_col_idx = i
                break
                
        if time_col_idx == -1:
            logger.warning("Time column not found, skipping time-based removal")
            return csv_data
            
        # Keep header and rows after specified minutes
        # Assuming format is "m:ss" (e.g., "0:15", "3:00")
        header = rows[0]
        filtered_rows = [header]
        
        for row in rows[1:]:
            if len(row) <= time_col_idx:
                continue  # Skip rows with insufficient columns
                
            time_str = row[time_col_idx]
            try:
                # Parse time (expected format "0:00" or "3:15")
                time_parts = time_str.split(':')
                if len(time_parts) != 2:
                    filtered_rows.append(row)  # Keep row if can't parse time
                    continue
                    
                minutes = int(time_parts[0])
                
                # Keep if minutes >= specified minutes to remove
                if minutes >= minutes_to_remove:
                    filtered_rows.append(row)
            except:
                # Keep row if can't parse time
                filtered_rows.append(row)
                
        # Convert back to CSV string
        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(filtered_rows)
        
        return output.getvalue()
    
    except Exception as e:
        logger.error(f"Error removing time range: {str(e)}")
        raise

@app.route('/api/calculate-rmr', methods=['POST'])
def calculate_rmr_api():
    """API endpoint for RMR calculation."""
    if not request.json or 'csv_data' not in request.json:
        return jsonify({'status': 'error', 'message': 'No CSV data provided'}), 400
    
    csv_data = request.json['csv_data']
    client_data = request.json.get('client_data', {}) or {}
    
    return calculate_rmr(csv_data, client_data)
    
def calculate_rmr(csv_data, client_data):
    """Calculate RMR metrics from CSV data."""
    try:
        # Parse CSV data
        client_data = client_data or {}
        
        # Create a CSV reader
        csv_reader = csv.reader(io.StringIO(csv_data))
        rows = list(csv_reader)
        
        if len(rows) < 3:  # Need at least header, units, and one data row
            return jsonify({'status': 'error', 'message': 'CSV file has insufficient data'}), 400
        
        # Extract data, skipping the units row (row[1])
        headers = rows[0]
        data_rows = rows[2:]  # Skip the units row
        
        # Find column indexes
        col_indexes = {
            'time': headers.index('Time') if 'Time' in headers else -1,
            'vo2_ml_min': headers.index('VO2') if 'VO2' in headers else -1,
            'vo2_ml_kg_min': headers.index('VO2') + 1 if 'VO2' in headers else -1,  # Assuming it's the next column
            'vco2_ml_min': headers.index('VCO2') if 'VCO2' in headers else -1,
            'vco2_ml_kg_min': headers.index('VCO2') + 1 if 'VCO2' in headers else -1,  # Assuming it's the next column
            'rer': headers.index('RER') if 'RER' in headers else -1
        }
        
        # Validate required columns exist
        if -1 in col_indexes.values():
            return jsonify({
                'status': 'error', 
                'message': 'Required columns not found in CSV. Needs: Time, VO2, VCO2, RER'
            }), 400
        
        # Extract numerical data for calculations
        vo2_values = []
        vco2_values = []
        rer_values = []
        
        for row in data_rows:
            if len(row) <= max(col_indexes.values()):
                continue  # Skip rows with insufficient columns
                
            try:
                vo2 = float(row[col_indexes['vo2_ml_min']])
                vco2 = float(row[col_indexes['vco2_ml_min']])
                rer = float(row[col_indexes['rer']])
                
                vo2_values.append(vo2)
                vco2_values.append(vco2)
                rer_values.append(rer)
            except (ValueError, IndexError) as e:
                logger.warning(f"Skipping row due to error: {e}")
                continue
        
        # Calculate averages
        avg_vo2 = np.mean(vo2_values) if vo2_values else 0
        avg_vco2 = np.mean(vco2_values) if vco2_values else 0
        avg_rer = np.mean(rer_values) if rer_values else 0
        
        # Calculate RMR in kcal/day (Weir equation)
        # RMR = (3.941 * VO2 + 1.106 * VCO2) * 1.44
        rmr_kcal_day = (3.941 * avg_vo2 + 1.106 * avg_vco2) * 1.44
        
        # Calculate substrate oxidation (g/day)
        # Fat oxidation = 1.67 * (VO2 - VCO2) * 1440
        # Carbohydrate oxidation = 4.55 * VCO2 - 3.21 * VO2 * 1440
        fat_oxidation = 1.67 * (avg_vo2 - avg_vco2) * 1.44  # g/day
        carb_oxidation = (4.55 * avg_vco2 - 3.21 * avg_vo2) * 1.44  # g/day
        # We're not calculating protein_oxidation anymore as requested
        
        # Calculate statistical metrics
        vo2_median = np.median(vo2_values)
        vco2_median = np.median(vco2_values)
        rer_median = np.median(rer_values)
        
        # Mode approximation (using histogram bins)
        vo2_mode = 0
        vco2_mode = 0
        rer_mode = 0
        if len(vo2_values) > 0:
            vo2_hist, vo2_bins = np.histogram(vo2_values, bins=10)
            vo2_mode_index = np.argmax(vo2_hist)
            vo2_mode = (vo2_bins[vo2_mode_index] + vo2_bins[vo2_mode_index+1]) / 2
            
            vco2_hist, vco2_bins = np.histogram(vco2_values, bins=10)
            vco2_mode_index = np.argmax(vco2_hist)
            vco2_mode = (vco2_bins[vco2_mode_index] + vco2_bins[vco2_mode_index+1]) / 2
            
            rer_hist, rer_bins = np.histogram(rer_values, bins=10)
            rer_mode_index = np.argmax(rer_hist)
            rer_mode = (rer_bins[rer_mode_index] + rer_bins[rer_mode_index+1]) / 2
        
        # Standard deviation
        vo2_std = np.std(vo2_values)
        vco2_std = np.std(vco2_values)
        rer_std = np.std(rer_values)
        
        # Sample size
        sample_size = len(vo2_values)
        
        # Coefficient of variation
        vo2_cv = (vo2_std / avg_vo2 * 100) if avg_vo2 else 0
        rer_cv = (rer_std / avg_rer * 100) if avg_rer else 0
        
        # 95% Confidence Intervals
        # Standard Error = std / sqrt(n)
        # 95% CI = mean ± (1.96 * SE)
        if sample_size > 1:
            vo2_se = vo2_std / np.sqrt(sample_size)
            vco2_se = vco2_std / np.sqrt(sample_size)
            rer_se = rer_std / np.sqrt(sample_size)
            
            vo2_ci_lower = avg_vo2 - (1.96 * vo2_se)
            vo2_ci_upper = avg_vo2 + (1.96 * vo2_se)
            
            vco2_ci_lower = avg_vco2 - (1.96 * vco2_se)
            vco2_ci_upper = avg_vco2 + (1.96 * vco2_se)
            
            rer_ci_lower = avg_rer - (1.96 * rer_se)
            rer_ci_upper = avg_rer + (1.96 * rer_se)
        else:
            vo2_ci_lower = vo2_ci_upper = avg_vo2
            vco2_ci_lower = vco2_ci_upper = avg_vco2
            rer_ci_lower = rer_ci_upper = avg_rer
        
        # Calculate RMR bounds based on VO2 CI
        rmr_lower_bound = (3.941 * vo2_ci_lower + 1.106 * avg_vco2) * 1.44
        rmr_upper_bound = (3.941 * vo2_ci_upper + 1.106 * avg_vco2) * 1.44
        
        # Calculate substrate bounds
        fat_lower_bound = 1.67 * (vo2_ci_lower - vco2_ci_upper) * 1.44
        fat_upper_bound = 1.67 * (vo2_ci_upper - vco2_ci_lower) * 1.44
        
        glucose_lower_bound = (4.55 * vco2_ci_lower - 3.21 * vo2_ci_upper) * 1.44
        glucose_upper_bound = (4.55 * vco2_ci_upper - 3.21 * vo2_ci_lower) * 1.44
        
        # Calculate predicted RMR based on client data
        predicted_rmr = 0
        rmr_percent_predicted = 0
        
        # Additional predictions
        cunningham_rmr = 0
        mifflin_rmr = 0 
        harris_benedict_rmr = 0
        
        if client_data.get('age') and client_data.get('gender') and client_data.get('weight_kg'):
            age = int(client_data['age'])
            gender = client_data['gender']
            weight_kg = float(client_data['weight_kg'])
            
            # Get height if provided, otherwise use defaults
            height_cm = float(client_data.get('height_cm', 170 if gender == 'MALE' else 160))
            
            # Estimate lean body mass (LBM) if not provided
            # Using rough estimation: Males ~85% of weight, Females ~75% of weight
            lean_body_mass = float(client_data.get('lean_body_mass', 
                                                   weight_kg * 0.85 if gender == 'MALE' else weight_kg * 0.75))
            
            # 1. Cunningham Equation: 500 + (22 * LBM)
            cunningham_rmr = 500 + (22 * lean_body_mass)
            
            # 2. Mifflin-St Jeor Equation
            if gender == 'MALE':
                mifflin_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
            else:  # FEMALE
                mifflin_rmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
            
            # 3. Harris-Benedict Equation (Revised)
            if gender == 'MALE':
                harris_benedict_rmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
            else:  # FEMALE
                harris_benedict_rmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
            
            # Calculate the average of the three predictions
            predicted_rmr = (cunningham_rmr + mifflin_rmr + harris_benedict_rmr) / 3
            
            # Calculate the percentage of measured RMR compared to the average predicted
            if predicted_rmr > 0:
                rmr_percent_predicted = (rmr_kcal_day / predicted_rmr) * 100
        
        # Prepare the results
        results = {
            'status': 'success',
            'rmr_kcal_day': round(rmr_kcal_day, 2),
            'vo2_avg': round(avg_vo2, 2),
            'vco2_avg': round(avg_vco2, 2),
            'rer_avg': round(avg_rer, 3),
            'predicted_rmr': round(predicted_rmr, 2),
            'rmr_percent_predicted': round(rmr_percent_predicted, 2),
            'fat_oxidation': round(fat_oxidation, 2),
            'carb_oxidation': round(carb_oxidation, 2),
            'cunningham_rmr': round(cunningham_rmr, 2),
            'mifflin_rmr': round(mifflin_rmr, 2), 
            'harris_benedict_rmr': round(harris_benedict_rmr, 2),
            
            # Statistical metrics
            'stats': {
                'vo2': {
                    'mean': round(avg_vo2, 2),
                    'median': round(vo2_median, 2),
                    'mode': round(vo2_mode, 2),
                    'stdev': round(vo2_std, 2),
                    'cv': round(vo2_cv, 2),
                    'sample_size': sample_size,
                    'ci_95': round(1.96 * vo2_std / np.sqrt(sample_size) if sample_size > 0 else 0, 2),
                    'lower_bound_95_ci': round(vo2_ci_lower, 2),
                    'upper_bound_95_ci': round(vo2_ci_upper, 2)
                },
                'rer': {
                    'mean': round(avg_rer, 3),
                    'median': round(rer_median, 3),
                    'mode': round(rer_mode, 3),
                    'stdev': round(rer_std, 3),
                    'cv': round(rer_cv, 2),
                    'sample_size': sample_size,
                    'ci_95': round(1.96 * rer_std / np.sqrt(sample_size) if sample_size > 0 else 0, 3),
                    'lower_bound_95_ci': round(rer_ci_lower, 3),
                    'upper_bound_95_ci': round(rer_ci_upper, 3)
                },
                'rmr': {
                    'lower_bound_95_ci_kcal_day': round(rmr_lower_bound, 2),
                    'upper_bound_95_ci_kcal_day': round(rmr_upper_bound, 2)
                },
                'substrate': {
                    'lower_bound_95_ci_glucose_g_day': round(glucose_lower_bound, 2),
                    'upper_bound_95_ci_glucose_g_day': round(glucose_upper_bound, 2),
                    'lower_bound_95_ci_fat_g_day': round(fat_lower_bound, 2),
                    'upper_bound_95_ci_fat_g_day': round(fat_upper_bound, 2)
                }
            },
            
            'raw_data': {
                'time_points': [row[col_indexes['time']] for row in data_rows if len(row) > col_indexes['time']],
                'vo2_values': vo2_values,
                'vco2_values': vco2_values,
                'rer_values': rer_values
            }
        }
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error calculating RMR: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error calculating RMR: {str(e)}'}), 500

@app.route('/api/save-client', methods=['POST'])
def save_client():
    """Save client data and RMR results."""
    if not request.json:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    try:
        data = request.json
        client_data = data.get('client_data', {})
        rmr_results = data.get('rmr_results', {})
        raw_data = data.get('raw_data', [])
        
        # Parse test date
        test_date = None
        if client_data.get('test_date'):
            try:
                test_date = datetime.strptime(client_data['test_date'], '%Y-%m-%d').date()
            except ValueError:
                test_date = None
        
        # Create or update client
        client_id = client_data.get('id')
        if client_id:
            client = Client.query.get(client_id)
            if not client:
                return jsonify({'status': 'error', 'message': 'Client not found'}), 404
        else:
            client = Client()
        
        # Update client data
        client.first_name = client_data.get('first_name', '')
        client.last_name = client_data.get('last_name', '')
        client.age = int(client_data.get('age', 0)) if client_data.get('age') else None
        client.gender = client_data.get('gender', '')
        client.weight_kg = float(client_data.get('weight_kg', 0)) if client_data.get('weight_kg') else None
        client.weight_lbs = float(client_data.get('weight_lbs', 0)) if client_data.get('weight_lbs') else None
        client.test_date = test_date
        
        # Update RMR results
        client.rmr_kcal_day = float(rmr_results.get('rmr_kcal_day', 0)) if rmr_results.get('rmr_kcal_day') else None
        client.vo2_avg = float(rmr_results.get('vo2_avg', 0)) if rmr_results.get('vo2_avg') else None
        client.vco2_avg = float(rmr_results.get('vco2_avg', 0)) if rmr_results.get('vco2_avg') else None
        client.rer_avg = float(rmr_results.get('rer_avg', 0)) if rmr_results.get('rer_avg') else None
        client.predicted_rmr = float(rmr_results.get('predicted_rmr', 0)) if rmr_results.get('predicted_rmr') else None
        client.rmr_percent_predicted = float(rmr_results.get('rmr_percent_predicted', 0)) if rmr_results.get('rmr_percent_predicted') else None
        client.fat_oxidation = float(rmr_results.get('fat_oxidation', 0)) if rmr_results.get('fat_oxidation') else None
        client.carb_oxidation = float(rmr_results.get('carb_oxidation', 0)) if rmr_results.get('carb_oxidation') else None
        client.protein_oxidation = float(rmr_results.get('protein_oxidation', 0)) if rmr_results.get('protein_oxidation') else None
        
        db.session.add(client)
        db.session.commit()
        
        # Save raw data points if provided
        if raw_data and len(raw_data) > 0:
            # First, remove any existing data points for this client
            RmrData.query.filter_by(client_id=client.id).delete()
            
            # Add new data points
            for row in raw_data:
                # Create new RmrData instance
                data_point = RmrData()
                
                # Set attributes
                data_point.client_id = client.id
                data_point.time_point = row.get('time_point', '')
                data_point.tidal_volume = float(row.get('tidal_volume', 0)) if row.get('tidal_volume') else None
                data_point.respiratory_rate = float(row.get('respiratory_rate', 0)) if row.get('respiratory_rate') else None
                data_point.vo2_ml_min = float(row.get('vo2_ml_min', 0)) if row.get('vo2_ml_min') else None
                data_point.vo2_ml_kg_min = float(row.get('vo2_ml_kg_min', 0)) if row.get('vo2_ml_kg_min') else None
                data_point.ve_vo2 = float(row.get('ve_vo2', 0)) if row.get('ve_vo2') else None
                data_point.feo2 = float(row.get('feo2', 0)) if row.get('feo2') else None
                data_point.vco2_ml_min = float(row.get('vco2_ml_min', 0)) if row.get('vco2_ml_min') else None
                data_point.vco2_ml_kg_min = float(row.get('vco2_ml_kg_min', 0)) if row.get('vco2_ml_kg_min') else None
                data_point.ve_vco2 = float(row.get('ve_vco2', 0)) if row.get('ve_vco2') else None
                data_point.feco2 = float(row.get('feco2', 0)) if row.get('feco2') else None
                data_point.rer = float(row.get('rer', 0)) if row.get('rer') else None
                db.session.add(data_point)
            
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Client data saved successfully',
            'client_id': client.id,
            'client': client.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error saving client data: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error saving client data: {str(e)}'}), 500

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Get a list of all clients."""
    try:
        clients = Client.query.order_by(Client.updated_at.desc()).all()
        return jsonify({
            'status': 'success',
            'clients': [client.to_dict() for client in clients]
        })
    except Exception as e:
        logger.error(f"Error retrieving clients: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error retrieving clients: {str(e)}'}), 500

@app.route('/api/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Get client data by ID."""
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'status': 'error', 'message': 'Client not found'}), 404
        
        # Get associated raw data
        raw_data = RmrData.query.filter_by(client_id=client_id).all()
        
        return jsonify({
            'status': 'success',
            'client': client.to_dict(),
            'raw_data': [data.to_dict() for data in raw_data]
        })
    except Exception as e:
        logger.error(f"Error retrieving client data: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error retrieving client data: {str(e)}'}), 500

@app.route('/api/generate-pdf-report', methods=['POST'])
def pdf_report_endpoint():
    return generate_pdf_report()

@app.route('/api/send-report-email', methods=['POST'])
def send_report_email_api():
    """Send RMR report via email to client."""
    if not request.json:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    try:
        from services.email_service import send_report_email, create_html_report
        
        # Get the client and report data
        client_data = request.json.get('clientData', {})
        report_data = request.json.get('reportData', {})
        
        # Validate client email
        client_email = client_data.get('email')
        if not client_email:
            return jsonify({'status': 'error', 'message': 'Client email address is required'}), 400
        
        # Check for SendGrid API key
        if not os.environ.get('SENDGRID_API_KEY'):
            return jsonify({
                'status': 'error', 
                'message': 'SendGrid API key is not configured. Please set the SENDGRID_API_KEY environment variable.'
            }), 400
        
        # Create email subject
        client_name = f"{client_data.get('firstName', '')} {client_data.get('lastName', '')}".strip()
        if not client_name:
            client_name = "Client"
        
        subject = f"Your RMR Assessment Results - {client_name}"
        
        # Create HTML email content
        html_content = create_html_report(client_data, report_data)
        
        # TODO: Generate PDF and attach (future enhancement)
        pdf_content = None
        
        # Send email
        response = send_report_email(
            to_email=client_email,
            subject=subject,
            html_content=html_content,
            pdf_content=pdf_content
        )
        
        if response.get('status') == 'success':
            return jsonify({
                'status': 'success',
                'message': 'Email sent successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f"Failed to send email: {response.get('message')}"
            }), 500
            
    except ImportError as e:
        logger.error(f"Email service module not found: {str(e)}")
        return jsonify({
            'status': 'error', 
            'message': 'Email service is not available. Please ensure the required modules are installed.'
        }), 500
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error sending email: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
