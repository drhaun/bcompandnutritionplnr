Core Application Files
main.py

Purpose: Entry point for the Flask application
Key Components: Imports the Flask app from app.py
Interactions: This is what Gunicorn uses to start the application server

app.py
Purpose: Core application logic and routes
Key Components:
Flask initialization and configuration
Database setup with SQLAlchemy
Route handlers for data processing

Key Routes:
/ and /body-composition: Serves the main assessment form
/save-body-composition: API endpoint that stores client data, 3D scan data, and ultrasound measurements
/api/process-csv: Handles CSV file processing with multi-step validation
Interactions: Communicates with the database through models.py and renders templates

models.py
Purpose: Defines database schema using SQLAlchemy ORM
Key Models:
Client: Stores client personal information and test results
RmrData: Stores raw resting metabolic rate data points
BodyCompositionData: Stores body composition measurements from 3D scans
UltrasoundData: Stores ultrasound measurement data
Interactions: Used by app.py to store and retrieve data from the database

app_routes.py
Purpose: Contains specialized routes, primarily for report generation
Key Functions: generate_pdf_report() - Creates PDF reports of body composition assessments
Interactions: Imported by app.py and uses services from pdf_service.py

Templates
templates/direct_entry.html
Purpose: Main user interface for body composition assessment
Key Sections:
Client information form
CSV upload for 3D scan and ultrasound data
3C-Model calculation interface
Results display tables
Interactions:
Loads JavaScript for calculations (3c-model-calculator.js, bmi-calculator.js)
Submits data to app.py endpoints
Displays calculation results in real-time

Static Files
static/js/3c-model-calculator.js
Purpose: Performs 3-Component model calculations for body composition
Key Functions:
calculate3CModel(): Calculates body fat percentage using body density and total body water
updateSiteInfo(): Updates interface based on selected measurement protocol
Interactions: Called from direct_entry.html when input values change or when calculation buttons are clicked
static/js/better-csv-viewer.js
Purpose: Handles CSV file visualization
Key Functions:
handleScanFile(): Processes 3D scan CSV files
handleUltrasoundFile(): Processes ultrasound measurement CSV files
displayBetterScanTable(): Renders scan data in a formatted table
Interactions: Called by file input handlers in direct_entry.html
static/js/bmi-calculator.js
Purpose: Calculates Body Mass Index
Key Functions: calculateBMI(): Computes BMI from height and weight
Interactions: Called when height or weight values change in the form
static/js/bmi-direct-fix.js
Purpose: Ensures BMI is calculated and displayed correctly
Key Functions: calculateAndDisplayBMI(): Updates BMI value in real-time
Interactions: Fixes timing issues with the original BMI calculator
static/css/base.css
Purpose: Core styling for the application
Key Styles: Defines colors, spacing, form layouts, and responsive design elements
Interactions: Loaded by all HTML templates

Services
services/pdf_service.py
Purpose: Generates PDF reports
Key Functions: generate_body_composition_report(): Creates branded PDF reports with client data
Interactions: Called by app_routes.py when a PDF report is requested
services/email_service.py
Purpose: Sends reports via email
Key Functions: send_report_email(): Emails reports to clients with optional PDF attachments
Interactions: Can be called by app.py routes when email functionality is needed

Data Flow
User enters client information in direct_entry.html
User can upload CSV files for 3D scan or ultrasound data
better-csv-viewer.js processes these files and displays them in tables
User can select records from these tables to use in calculations
When values are entered or selected:
bmi-calculator.js calculates BMI
3c-model-calculator.js performs 3C-Model calculations
User can save data using the Save button, which:
Sends data to /save-body-composition endpoint in app.py
app.py processes this data and stores it using models defined in models.py
For RMR data processing (if used):
CSV files are sent to /api/process-csv endpoint
app.py processes these in multiple steps (removing units row, filtering data)
Results are stored in the database using RmrData model
This architecture follows a standard Flask application pattern with clear separation of concerns between routes, models, and services. The JavaScript files enhance the user experience by providing real-time calculations and data visualization without requiring page reloads.
