from flask import request, jsonify, Blueprint
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import json

from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()



uploads= Blueprint('uploads', __name__)

with open(os.path.join(os.path.dirname(__file__), "uploadrequirements.json"), 'r') as f:
    upload_requirements = json.load(f)


"""
This is to get all the branches and course codes
"""
@uploads.route('/branches', methods=['GET'])
def get_branches():
    branches=upload_requirements.get('Branch',{}).get('Branch', [])
    print("Branches:", branches)
    return jsonify({'branches': branches})

"""
This is to get all the course coades for a given semester and branch
"""
@uploads.route('/subject-codes', methods=['GET'])
def get_subject_codes():
    
    semester = request.args.get('semester')
    branch = request.args.get('branch')

    # Corrected way to access the nested dictionary
    semester_data = upload_requirements.get(semester, {})
    subject_codes = semester_data.get('Subject Codes', {}).get(branch, [])

    print(subject_codes)
    return jsonify({'subject_codes': subject_codes})


"""



"""
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

# print("Client ID:", CLIENT_ID)
# print("Client Secret:", CLIENT_SECRET)
# print("Refresh Token:", REFRESH_TOKEN)


def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    print("Status:", response.status_code)
    print("Response:", response.text)  # This will show Google’s actual error
    if response.ok:
        return response.json().get("access_token")
    return None


@uploads.route('/get-presigned-url', methods=['POST'])
@jwt_required()
def get_presigned_url():
    file_metadata = request.json
    filename = file_metadata.get('originalFileName', 'untitled.pdf')
    mime_type = file_metadata.get('mimeType', 'application/pdf')
    from .dbmodels import Users
    current_user = get_jwt_identity()
    
    user= Users.query.filter_by(and_id=current_user).first()
    if user.user_type not in ['MAINTAINER','DEVELOPER']:
        return jsonify({'error': 'Please Contact Developer to Become maintainer to upload'}), 403
    access_token = get_access_token()
    print("Access Token:", access_token)
    if not access_token:
        return jsonify({"error": "Failed to get access token"}), 500

    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": mime_type
        }

    metadata = {
            "name": filename,
            "parents": ["root"]  # or your Shared Drive ID
        }

    res = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
            headers=headers,
            json=metadata
        )

    if res.status_code == 200:
        upload_url = res.headers['Location']
        return jsonify({"uploadUrl": upload_url, "token": access_token})
    else:
        return jsonify({"error": "Failed to get upload URL", "details": res.text}), 500

    


@uploads.route('/save-metadata', methods=['POST'])
@jwt_required()
def save_metadata():
    from .dbmodels import MaterialMetadata, Users
    from .Main import db
    data = request.json
    current_user = get_jwt_identity()
    
    user = Users.query.filter_by(and_id=current_user).first()
    if not user:
        return jsonify({'error': 'Invalid user'}), 404
    
    # Ensure upload_requirements is accessible and correctly structured
    subject_name = upload_requirements.get('Subject_name', {}).get(data.get('subjectCode'), ['Unknown Subject'])[0]
    

    try:
        new_material = MaterialMetadata(
            and_id=current_user,
            semester=data.get('semester'),
            branch=data.get('branch'),
            upload_type=data.get('uploadType'),
            subject_code=data.get('subjectCode'),
            details=data.get('details'),
            original_file_name=data.get('originalFileName'),
            s3_key=data.get('s3Key'), # Assuming this is meant to store the Google Drive File ID now
            subject_name=subject_name,
            description=data.get('description')
        )

        db.session.add(new_material)
        db.session.commit()

        return jsonify({'message': 'Metadata saved successfully'}), 201

    except Exception as e:
        db.session.rollback()
        
        return jsonify({'error': 'Failed to save metadata'}), 500
    
@uploads.route("/proxy-upload-to-google", methods=["POST"])
def proxy_upload_form():
    # data=response = request.form
    # print("Received data:", data)
    
    upload_url = request.form.get("uploadUrl")
    print("Upload URL:", upload_url)
    file = request.files.get("file")
    if not upload_url or not file:
        return jsonify({"error": "Missing upload URL or file"}), 400
    

    res = requests.put(upload_url, data=file, headers={
            "Content-Type":"application/pdf",
        })

    if not res.ok:
            
        return jsonify({"error": "Failed to upload to Google"}), res.status_code
    finalize_upload(res.json().get("id"))
    id= res.json().get("id")
    return jsonify({"success": True,"id":id}), 200
   

    

def finalize_upload(file_id):
    try:
        access_token = get_access_token()
        if not access_token:
            return jsonify({"error": "Failed to get access token"}), 500

        # Step 1: Make the file public
        perm_res = requests.post(
            f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "role": "reader",
                "type": "anyone"
            }
        )

        if perm_res.status_code not in [200, 204]:
            return jsonify({"error": "Failed to set permissions", "details": perm_res.text}), 500

        # Step 2: Return public link
        public_url = f"https://drive.google.com/file/d/{file_id}/view"
        return jsonify({
            "success": True,
            "fileId": file_id,
            "publicUrl": public_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@uploads.route('/save-placement-metadata', methods=['POST'])
@jwt_required()
def save_placement_metadata():
    from .dbmodels import PlacementMaterialMetadata, Users
    from .Main import db
    data = request.json
    current_user = get_jwt_identity()
    
    user = Users.query.filter_by(and_id=current_user).first()
    if not user:
        return jsonify({'error': 'Invalid user'}), 404
    
    # Ensure upload_requirements is accessible and correctly structured
    

    try:
        new_material = PlacementMaterialMetadata(
            and_id=current_user,
            type=data.get('type'),
            category=data.get('category'),
            details=data.get('details'),
            original_file_name=data.get('originalFileName'),
            file_url=data.get('fileUrl'), 
            description=data.get('description')
        )

        db.session.add(new_material)
        db.session.commit()

        return jsonify({'message': 'Metadata saved successfully'}), 201

    except Exception as e:
        db.session.rollback()
        
        return jsonify({'error': 'Failed to save metadata'}), 500
    
