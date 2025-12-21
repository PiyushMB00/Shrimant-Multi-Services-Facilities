from flask import Flask, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Initialize Flask App
# We set static_folder and template_folder to '.' to serve files from the root directory
# This allows us to keep the current file structure (index.html in root) 
app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

# --- CONFIGURATION ---
# REPLACE THESE WITH YOUR ACTUAL CREDENTIALS
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'shrimantmultiservices79@gmail.com'
SENDER_PASSWORD = 'wqxe eovp jzxk hfph'  # Use an App Password, NOT your real password
RECEIVER_EMAIL = 'shrimantmultiservices79@gmail.com' # Where you want to receive notifications

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/send-email', methods=['POST'])
def handle_email_submission():
    data = request.json
    
    full_name = data.get('full_name')
    email = data.get('email')
    phone = data.get('mobile')
    message = data.get('message')

    # 1. Send Notification to Admin
    admin_subject = f"New Contact Form Submission from {full_name}"
    admin_body = f"""
    New Contact Form Submission:
    -----------------------------------
    Name: {full_name}
    Email: {email}
    Phone: {phone}
    
    Message:
    {message}
    -----------------------------------
    """
    admin_sent = send_email(RECEIVER_EMAIL, admin_subject, admin_body)

    # 2. Send Auto-Reply to User
    user_sent = False
    if email:
        user_subject = "Thank you for contacting Shrimant Multi Services"
        user_body = f"""
Hello {full_name},

Thank you for contacting Shrimant Multi Services. We truly appreciate you taking the time to reach out to us and for showing interest in our services.

This is to inform you that our team has successfully received your message. We are currently reviewing the details you have shared, and one of our representatives will get back to you shortly with the required information, guidance, or assistance. Please be assured that we aim to respond as promptly and accurately as possible.

If your inquiry requires any additional clarification or urgent attention, feel free to reply to this email with further details, and we will be happy to assist you.

Thank you once again for connecting with us. We value your interest and look forward to assisting you.

Warm regards,
Shrimant Multi Services
    """
        user_sent = send_email(email, user_subject, user_body)

    if admin_sent:
        return jsonify({"status": "success", "message": "Email sent successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send email"}), 500

if __name__ == '__main__':
    # print(f"Server running at http://127.0.0.1:5000")
    # print(f"Make sure to update SENDER_EMAIL and SENDER_PASSWORD in app.py")
    app.run(debug=True, port=5000)
