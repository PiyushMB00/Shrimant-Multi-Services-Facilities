from flask import Flask, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import requests

load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

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

def submit_to_google_form_background(form_url, payload):
    """Sends data directly to a Google Form in the background."""
    def _send():
        try:
            # Google Forms expects standard form-encoded data, not JSON
            response = requests.post(form_url, data=payload, timeout=10)
            if response.status_code == 200:
                print("Successfully saved to Google Forms!")
            else:
                print(f"Google Forms error: Status {response.status_code}")
        except Exception as e:
            print(f"Failed to submit to Google Forms: {e}")
            
    threading.Thread(target=_send, daemon=True).start()

def upload_file_to_storage(file, key, form_data):
    """Upload a single file to Supabase storage"""
    try:
        import werkzeug
        safe_filename = werkzeug.utils.secure_filename(file.filename)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        mobile = form_data.get('mobile', 'unknown')
        storage_path = f"{mobile}/{timestamp}_{key}_{safe_filename}"
        file_content = file.read()
        
        res = supabase.storage.from_("worker-documents").upload(
            path=storage_path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        
        public_url = supabase.storage.from_("worker-documents").get_public_url(storage_path)
        return {key: public_url}
    except Exception as upload_error:
        print(f"File upload error for {key}: {upload_error}")
        return {key: None}

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# --- WORKER REGISTRATION ROUTE ---
@app.route('/api/submit-worker-registration', methods=['POST'])
def handle_worker_registration():
    if not supabase:
        print("Supabase not configured")
        return jsonify({"status": "error", "message": "Backend database not configured"}), 500

    try:
        form_data = request.form.to_dict()
        files = request.files
        file_urls = {}

        # 1. Upload Files to Supabase
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            for key in request.files:
                file = files.get(key)
                if file and file.filename != '':
                    futures[executor.submit(upload_file_to_storage, file, key, form_data)] = key
            
            for future in as_completed(futures):
                result = future.result()
                file_urls.update(result)

        # 2. Save Text & URLs to Supabase Database
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
            "aadhar_url": file_urls.get('aadharFile'),
            "photo_url": file_urls.get('photoFile'),
            "address_proof_url": file_urls.get('addressProofFile'),
            "accepted_terms": True,
            "created_at": datetime.datetime.now().isoformat()
        }
        supabase.table("worker_registrations").insert(db_record).execute()
        
        # 3. Submit to Google Forms
        # IMPORTANT: Replace YOUR_FORM_ID with the actual ID from your form link.
        # Make sure the URL ends in /formResponse
        worker_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdc2sGb7Fjmv5H6RT-kstzh2k3vI6cTYVVqJU0swMqZWFTz9g/viewform?usp=publish-editor"
        
        # IMPORTANT: Replace these entry numbers with the ones you copied from the pre-filled link!
        google_payload = {
            "entry.1567162511": db_record['full_name'],
            "entry.1567162511": db_record['mobile'],
            "entry.1567162511": db_record['city'],
            "entry.1567162511": db_record['work_type'],
            "entry.1567162511": db_record['years_experience'],
            # You can even pass the Supabase file links straight into the Google Form!
            "entry.1567162511": db_record['aadhar_url'] or "No Aadhar uploaded" 
        }
        
        submit_to_google_form_background(worker_form_url, google_payload)

        return jsonify({"status": "success", "message": "Registration submitted successfully"}), 200

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)