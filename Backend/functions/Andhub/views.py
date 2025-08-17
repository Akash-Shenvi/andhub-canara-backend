from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity




import requests
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
views= Blueprint('views', __name__)



@views.route('/get-notes-subjectcode', methods=['GET'])
# @jwt_required()
def get_notes():
    from .dbmodels import MaterialMetadata
    

    semester = request.args.get('semester')
    branch = request.args.get('branch')
    upload_type = request.args.get('upload_type')

    print(f"Semester: {semester}, Branch: {branch}, Upload Type: {upload_type}")
    
    if not semester or not branch or not upload_type:
        return jsonify({'error': 'Missing semester, branch, or upload_type'}), 400

    # Get distinct subject_code + subject_name pairs
    subjects = (
        MaterialMetadata.query
        .filter_by(semester=semester, branch=branch, upload_type=upload_type)
        .with_entities(MaterialMetadata.subject_code, MaterialMetadata.subject_name)
        .distinct()
        .all()
    )

    # Format as list of dicts
    subject_list = [
        {"code": code, "name": name or "Unknown"}
        for code, name in subjects
    ]

    return jsonify({'subjects': subject_list}), 200


@views.route('/get_materials', methods=['POST'])
def get_materials():
    from .dbmodels import MaterialMetadata
    data = request.get_json()
    semester = data.get("semester")
    branch = data.get("branch")
    subject_code = data.get("subjectCode")

    materials = MaterialMetadata.query.filter_by(
        semester=semester,
        branch=branch,
        subject_code=subject_code
    ).all()

    result = []

    for mat in materials:
        file_id = mat.s3_key  # now used for Google Drive file ID

        # Refresh token if needed
      

        # Generate shareable view link
        view_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"

        result.append({
            "id": mat.id,
            "url": view_link,
            "details": mat.details,
            "description": mat.description,
            "type": "pdf"
        })

    return jsonify({"materials": result})





"""
This is to get the metadata of the uploaded material to Display Only if he is maintainer or developer .
"""
@views.route('/get_materials_admin', methods=['POST'])
@jwt_required()
def get_materials_admin():
    from .dbmodels import MaterialMetadata, Users
    current_user = get_jwt_identity()
    user = Users.query.filter_by(and_id=current_user).first()

    if user.user_type not in ['MAINTAINER', 'DEVELOPER']:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()
    semester = data.get('semester')
    branch = data.get('branch')
    upload_type = data.get('upload_type')

    if not all([semester, branch, upload_type]):
        return jsonify({"error": "Missing fields"}), 400

    query = MaterialMetadata.query.filter_by(
        semester=semester,
        branch=branch,
        upload_type=upload_type
    ).all()

    materials = []
    for record in query:
        file_id = record.s3_key  # now stores Google Drive file ID

        # Build Google Drive view URL (assumes public link access)
        view_url = f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"

        # Optional: if you want direct download link instead
        # download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

        materials.append({
            "id": record.id,
            "and_id": record.and_id,
            "semester": record.semester,
            "branch": record.branch,
            "upload_type": record.upload_type,
            "subject_code": record.subject_code,
            "details": record.details,
            "s3_key": file_id,
            "original_file_name": record.original_file_name,
            "url": view_url,  # use this in frontend
            "description": record.description
        })

    return jsonify({"materials": materials})

"""
This is to delete the uploaded material from the S3 bucket.
It will also delete the metadata from the database.
Only a maintainer or developer can delete the material.

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
    if response.ok:
        return response.json()['access_token']
    return None

@views.route('/download/<material_id>', methods=['GET'])
def download_material(material_id):
    # Step 1: Get material metadata from your database
    from .dbmodels import MaterialMetadata
    material = MaterialMetadata.query.filter_by(id=material_id).first()
    if not material:
        return jsonify({"error": "Material not found"}), 404

    # This is the Google Drive File ID you stored in your database
    file_id = material.s3_key 
    filename = material.original_file_name or "downloaded_file"
    
    session = requests.Session()
    base_url = f"https://drive.usercontent.google.com/u/0/uc?id={file_id}&export=download"
    return jsonify({"downloadUrl":base_url})
    # IMPORTANT CHANGE HERE 👇
   
@views.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_material(id):
    from .dbmodels import MaterialMetadata, Users
    from .Main import db
    from google.auth.transport.requests import Request

    current_user = get_jwt_identity()
    user = Users.query.filter_by(and_id=current_user).first()

    if user.user_type not in ['MAINTAINER', 'DEVELOPER']:
        return jsonify({'error': 'Access denied'}), 403

    record = MaterialMetadata.query.get(id)
    if not record:
        return jsonify({"error": "Material not found"}), 404

    file_id = record.s3_key  # stores Drive file ID

    try:
        access_token = get_access_token()
        if not access_token:
            return jsonify({"error": "Could not refresh token"}), 500

        # Delete file via HTTP API
        delete_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?supportsAllDrives=true"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        res = requests.delete(delete_url, headers=headers)

        if res.status_code in [200, 204]:
            db.session.delete(record)
            db.session.commit()
            return jsonify({"message": "Material deleted successfully"})
        else:
            return jsonify({
                "error": "Failed to delete from Google Drive",
                "details": res.text
            }), res.status_code

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Exception: {str(e)}"}), 500

    
@views.route('/update/<int:material_id>', methods=['PUT'])
@jwt_required()  # Require token if using JWT auth
def update_material(material_id):
    data = request.json
    from .dbmodels import MaterialMetadata
    from .Main import db
    material = MaterialMetadata.query.get(material_id)
    if not material:
        return jsonify({"error": "Material not found"}), 404

    try:
        material.semester = data.get('semester', material.semester)
        material.branch = data.get('branch', material.branch)
        material.upload_type = data.get('upload_type', material.upload_type)
        material.subject_code = data.get('subject_code', material.subject_code)
        material.details = data.get('details', material.details)
        material.description = data.get('description', material.description)
        material.original_file_name = data.get('original_file_name', material.original_file_name)

        db.session.commit()
        return jsonify({"message": "Material updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    
@views.route('/get_placement_materials', methods=['GET'])
def get_placement_materials():
    from .dbmodels import PlacementMaterialMetadata
    from .Main import db
    type = request.args.get("type")
    materials = (
        PlacementMaterialMetadata.query.filter_by(type=type)
        .with_entities(PlacementMaterialMetadata.category,).distinct()
        .all()
    )
    print(materials)
    return jsonify({"categories": [m.category for m in materials]}), 200

@views.route('/get-aptitude-materials', methods=['POST'])
def get_aptitude_materials():
    from .dbmodels import PlacementMaterialMetadata
    data = request.get_json()
    category = data.get("category")

    materials = PlacementMaterialMetadata.query.filter_by(
        category=category
    ).all()

    result = []
    for mat in materials:
        file_id = mat.file_url
        view_link = f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"
        result.append({
            "id": mat.id,
            "url": view_link,
            "details": mat.details,
            "description": mat.description,
            "type": "pdf"
        })

    return jsonify({"materials": result})


@views.route('/download-placement/<material_id>', methods=['GET'])
def download_material_placement(material_id):
    # Step 1: Get material metadata from your database
    from .dbmodels import PlacementMaterialMetadata
    material = PlacementMaterialMetadata.query.filter_by(id=material_id).first()
    if not material:
        return jsonify({"error": "Material not found"}), 404

    # This is the Google Drive File ID you stored in your database
    file_id = material.file_url 
    
    
    base_url = f"https://drive.usercontent.google.com/u/0/uc?id={file_id}&export=download"
    return jsonify({"downloadUrl":base_url})    