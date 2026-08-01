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
            # Mask the request as a normal Google Chrome browser
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.post(form_url, data=payload, headers=headers, timeout=10)
            
            if "freebirdFormviewerViewItemsItemErrorMessage" in response.text:
                print("❌ Google Forms REJECTED the data! A required field was missing or formatted incorrectly.")
            elif response.status_code == 200:
                print("✅ Successfully saved to Google Forms!")
            else:
                print(f"❌ Google Forms error: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Failed to submit to Google Forms: {e}")
            
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
        
       # --- GOOGLE FORMS SUBMISSION ---
        worker_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdc2sGb7Fjmv5H6RT-kstzh2k3vI6cTYVVqJU0swMqZWFTz9g/formResponse"
        
        # 1. Translate boolean checkboxes to Yes/No
        travel_status = "Yes" if db_record['willing_to_travel'] else "No"
        terms_status = "Yes" if db_record['accepted_terms'] else "No"
        
        # 2. Map HTML lowercase values to exact Google Form Text
        work_map = {
            "painter": "Painter",
            "photographer": "Photographer",
            "event": "Event Staff",
            "helper": "Interior Helper",
            "skilled": "Skilled Worker",
            "consultant": "Consultant",
            "other": "Other"
        }
        skill_map = {
            "helper": "Helper",
            "skilled": "Skilled",
            "expert": "Expert"
        }
        avail_map = {
            "daily": "Daily Work", # Updated to match your exact link!
            "short": "Short-term Contract",
            "long": "Long term contract"
        }

        # 3. Build the Payload (Ensuring NO required fields are completely blank)
        google_payload = {
            "entry.832184240": db_record['full_name'] or "Unknown",
            "entry.324331670": db_record['mobile'] or "0000000000",
            "entry.245043526": db_record['alt_mobile'] or "N/A",
            "entry.71665854": db_record['city'] or "N/A",
            "entry.650466239": db_record['area'] or "N/A",
            "entry.1221384629": db_record['date_of_birth'] or "2000-01-01",
            "entry.1838657915": work_map.get(db_record['work_type'], "Consultant"),
            "entry.595725800": skill_map.get(db_record['skill_level'], "Helper"),
            "entry.2103659760": str(db_record['years_experience']) if db_record['years_experience'] else "0",
            "entry.2117246788": db_record['tools'] or "None",
            "entry.1567162511": avail_map.get(db_record['availability'], "Daily Work"),
            "entry.1251137304": travel_status,
            "entry.1015867944": db_record['aadhar_url'] or "No Aadhar uploaded",
            "entry.1762161917": db_record['photo_url'] or "No photo uploaded",
            "entry.2114520497": db_record['address_proof_url'] or "No address uploaded",
            "entry.1580570584": db_record['bank_details'] or "N/A",
            "entry.1526165345": terms_status
        }
        
        submit_to_google_form_background(worker_form_url, google_payload)

        return jsonify({"status": "success", "message": "Registration submitted successfully"}), 200

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)