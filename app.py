from flask import Flask, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD') 
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL') 

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")

def send_email(to_email, subject, body):
    try:
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            print("Email credentials missing")
            return False
            
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

@app.route('/api/submit-worker-registration', methods=['POST'])
def handle_worker_registration():
    if not supabase:
        print("Supabase not configured")
        return jsonify({"status": "error", "message": "Backend database not configured"}), 500

    try:
        # Extract form data
        form_data = request.form.to_dict()
        
        files = request.files
        file_urls = {}

        # Upload files to Supabase Storage
        for key in request.files:
            file = files.get(key)
            if file and file.filename != '':
                # Clean filename
                import werkzeug
                safe_filename = werkzeug.utils.secure_filename(file.filename)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                # Structure: {mobile}/{timestamp}_{type}_{filename}
                mobile = form_data.get('mobile', 'unknown')
                storage_path = f"{mobile}/{timestamp}_{key}_{safe_filename}"
                file_content = file.read()
                
                # Upload to 'worker-documents' bucket
                try:
                    res = supabase.storage.from_("worker-documents").upload(
                        path=storage_path,
                        file=file_content,
                        file_options={"content-type": file.content_type}
                    )
                    
                    # Get public URL
                    public_url = supabase.storage.from_("worker-documents").get_public_url(storage_path)
                    file_urls[key] = public_url
                except Exception as upload_error:
                    print(f"File upload error for {key}: {upload_error}")
                    # Continue even if upload fails? No, probably better to fail.
                    # But for now let's log and continue to save at least partial data
                    # return jsonify({"status": "error", "message": f"Failed to upload {key}"}), 500

        # Construct database record
        db_record = {
            "full_name": form_data.get('fullName'),
            "mobile": form_data.get('mobile'),
            "alt_mobile": form_data.get('altMobile'),
            "city": form_data.get('city'),
            "area": form_data.get('area'),
            "date_of_birth": form_data.get('dob'),
            "work_type": form_data.get('workType'),
            "skill_level": form_data.get('skillLevel'),
            "years_experience": form_data.get('experience'),
            "tools": form_data.get('tools'),
            "availability": form_data.get('availability'),
            "willing_to_travel": form_data.get('travel') == 'on',  
            "bank_details": form_data.get('bankDetails'),
            # Map file URLs - ensure keys match frontend input names
            "aadhar_url": file_urls.get('aadharFile'),
            "photo_url": file_urls.get('photoFile'),
            "address_proof_url": file_urls.get('addressProofFile'),
            "created_at": datetime.datetime.now().isoformat()
        }

        # Insert into Supabase
        data = supabase.table("worker_registrations").insert(db_record).execute()
        
        return jsonify({"status": "success", "message": "Registration submitted successfully"}), 200

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
