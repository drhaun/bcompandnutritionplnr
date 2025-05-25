"""
PDF Report Generation Service
Generates branded PDF reports for body composition assessments
"""

import pdfkit
import os
import base64
import io
from datetime import datetime
from flask import render_template, current_app

def generate_body_composition_report(client_data, scan_data=None, ultrasound_data=None, 
                                     body_density=None, body_fat_results=None):
    """
    Generate a complete PDF report for body composition assessment
    
    Args:
        client_data (dict): Client personal information and metrics
        scan_data (dict, optional): 3D scan data results
        ultrasound_data (dict, optional): Ultrasound measurement data
        body_density (float, optional): Calculated body density
        body_fat_results (dict, optional): Body fat calculation results
        
    Returns:
        bytes: PDF file as bytes
    """
    try:
        # Prepare client info
        client_info = {
            'name': f"{client_data.get('first_name', '')} {client_data.get('last_name', '')}",
            'age': client_data.get('age', ''),
            'gender': client_data.get('gender', ''),
            'height_cm': client_data.get('height_cm', ''),
            'height_in': client_data.get('height_in', ''),
            'weight_kg': client_data.get('weight_kg', ''),
            'weight_lbs': client_data.get('weight_lbs', ''),
            'test_date': client_data.get('test_date', datetime.now().strftime('%Y-%m-%d')),
        }
        
        # Get water data
        water_data = {
            'water_percent1': client_data.get('water_percent1', ''),
            'water_percent2': client_data.get('water_percent2', ''),
            'water_percent3': client_data.get('water_percent3', ''),
            'water_device1': client_data.get('water_device1', ''),
            'water_device2': client_data.get('water_device2', ''),
            'water_device3': client_data.get('water_device3', ''),
            'water_liters1': client_data.get('water_liters1', ''),
            'water_liters2': client_data.get('water_liters2', ''),
            'water_liters3': client_data.get('water_liters3', ''),
            'water_liters_avg': client_data.get('water_liters_avg', ''),
            'water_liters_final': client_data.get('water_liters_final', ''),
            'specific_gravity': client_data.get('specific_gravity', ''),
        }
        
        # Organize 3C-Model results
        model_results = {}
        if body_fat_results:
            model_results = {
                'body_fat': body_fat_results.get('body_fat_3c', ''),
                'fat_mass_kg': body_fat_results.get('fat_mass_kg', ''),
                'fat_mass_lbs': body_fat_results.get('fat_mass_lbs', ''),
                'ffm_kg': body_fat_results.get('ffm_kg', ''),
                'ffm_lbs': body_fat_results.get('ffm_lbs', ''),
                'fmi': body_fat_results.get('fmi', ''),
                'ffmi': body_fat_results.get('ffmi', ''),
                'body_density': body_density or '',
            }
        
        # Get logos and branding
        logo_path = os.path.join('static', 'img', 'fitomics_logo.png')
        if not os.path.isfile(os.path.join(current_app.root_path, logo_path)):
            logo_path = os.path.join('attached_assets', 'Fitomics Logomark – Dark Blue.png')
        
        # Render HTML template
        html_content = render_template(
            'report_template.html',
            client=client_info,
            water=water_data,
            scan=scan_data,
            ultrasound=ultrasound_data,
            model_results=model_results,
            report_date=datetime.now().strftime('%Y-%m-%d'),
            logo_path=logo_path
        )
        
        # Configure PDF options
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': '',
        }
        
        # Generate PDF
        pdf_content = pdfkit.from_string(html_content, False, options=options)
        
        return pdf_content
        
    except Exception as e:
        current_app.logger.error(f"Error generating PDF report: {str(e)}")
        raise

def encode_image_base64(image_path):
    """
    Encode an image file as base64 string
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image string
    """
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        current_app.logger.error(f"Error encoding image: {str(e)}")
        return ""