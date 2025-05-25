"""
Email service for sending RMR reports
"""
import os
import sys
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId, Email,
    To, Subject, PlainTextContent, HtmlContent
)

def send_report_email(to_email, subject, html_content, pdf_content=None, from_email="reports@fitomics.com"):
    """
    Send an email with the RMR report
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_content (str): HTML content of the email
        pdf_content (bytes, optional): PDF report content as bytes
        from_email (str, optional): Sender email address
        
    Returns:
        dict: Response from SendGrid API
    """
    # Check for SendGrid API key
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        raise ValueError("SENDGRID_API_KEY environment variable is not set")
    
    # Create message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    # Add PDF attachment if provided
    if pdf_content:
        encoded_content = base64.b64encode(pdf_content).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded_content)
        attachment.file_name = FileName('rmr_report.pdf')
        attachment.file_type = FileType('application/pdf')
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('rmr_report')
        message.add_attachment(attachment)
    
    # Send email
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return {
            'status': 'success',
            'status_code': response.status_code,
            'message': 'Email sent successfully'
        }
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return {
            'status': 'error',
            'message': str(e)
        }

def create_html_report(client_data, report_data):
    """
    Create HTML content for the email
    
    Args:
        client_data (dict): Client information
        report_data (dict): RMR report data
        
    Returns:
        str: HTML content
    """
    client_name = f"{client_data.get('firstName', '')} {client_data.get('lastName', '')}".strip()
    if not client_name:
        client_name = "Client"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3a5a7d; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }}
            .content {{ padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #777; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Fitomics Fitness Lab</h1>
            <h2>Resting Metabolic Rate Assessment</h2>
        </div>
        
        <div class="content">
            <p>Dear {client_name},</p>
            
            <p>{client_data.get('message', 'Thank you for completing your Resting Metabolic Rate (RMR) assessment with Fitomics Fitness Lab. Attached is your detailed report and below is a summary of your results.')}</p>
            
            <h3>RMR Assessment Results</h3>
            
            <table>
                <tr>
                    <th>Measurement</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Measured RMR</td>
                    <td>{report_data.get('rmr', 'N/A')} kcal/day</td>
                </tr>
                <tr>
                    <td>Average VO2</td>
                    <td>{report_data.get('vo2', 'N/A')} ml/min</td>
                </tr>
                <tr>
                    <td>Average RER</td>
                    <td>{report_data.get('rer', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Fat Oxidation</td>
                    <td>{report_data.get('fatOxidation', 'N/A')} g/day</td>
                </tr>
                <tr>
                    <td>Carbohydrate Oxidation</td>
                    <td>{report_data.get('carbOxidation', 'N/A')} g/day</td>
                </tr>
            </table>
            
            <p>This information can help guide your nutrition and exercise strategies to better align with your metabolic profile and health goals.</p>
            
            <p>For a comprehensive breakdown of your results, please see the attached PDF report.</p>
            
            <p>If you have any questions about your assessment or would like to schedule a follow-up consultation, please don't hesitate to contact us.</p>
            
            <p>Best regards,<br>
            Fitomics Fitness Lab Team<br>
            <a href="mailto:contact@fitomics.com">contact@fitomics.com</a></p>
        </div>
        
        <div class="footer">
            <p>This email and any files transmitted with it are confidential and intended solely for the use of the individual or entity to whom they are addressed.</p>
            <p>&copy; 2025 Fitomics Fitness Lab. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    return html