from flask import send_file, request, jsonify
import io
from datetime import datetime
import json
import logging

# PDF generation route
def generate_pdf_report():
    """Generate a PDF report for body composition."""
    try:
        # Check if request contains data
        if not request.json:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
        # Get data from request
        data = request.json
        client_data = data.get('client_data', {})
        scan_data = data.get('scan_data', {})
        ultrasound_data = data.get('ultrasound_data', {})
        body_density = data.get('body_density')
        body_fat_results = data.get('body_fat_results', {})
        
        # Import PDF service
        from services.pdf_service import generate_body_composition_report
        
        # Generate PDF
        pdf_content = generate_body_composition_report(
            client_data, 
            scan_data, 
            ultrasound_data, 
            body_density,
            body_fat_results
        )
        
        # Generate filename based on client name and date
        client_name = f"{client_data.get('first_name', '')}_{client_data.get('last_name', '')}".strip()
        if not client_name:
            client_name = "Client"
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"Body_Composition_{client_name}_{date_str}.pdf"
        
        # Return PDF as download
        return send_file(
            io.BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logging.error(f"Error generating PDF report: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error generating PDF: {str(e)}'}), 500