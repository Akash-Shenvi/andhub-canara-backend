"""
This file contains p url endpoints related to render the front end.

"""

# Flask imports 
from flask import Blueprint
from flask import request,jsonify

from flask_jwt_extended import get_jwt_identity,jwt_required

pages=Blueprint('pages',__name__)

@pages.route('/dashboard',methods=['POST'])
@jwt_required()
def DashBoard():
    """
    Used to collect all the essential data need to be on the Dashboard of the user from all the gate way of the website.
    Inputs:
            Takes the input from the current users in the session.

    Outputs:
            1.name of the user, json variable name = name,
            2.USN of the user, json variable name = usn,
            3.email of the user, json variable name = email,
            4.Branch of the user, json variable name = Branch,
            5.phone number of the user,json variable name = phone no. 
    """
    from .dbmodels import Users
    try:
        current_user_id=get_jwt_identity()
        current_user=Users.query.filter_by(and_id=current_user_id).first()
        print(f"1:{current_user.and_id} 2:{current_user.name} 3:{current_user.USN} 4:{current_user.email} 5:{current_user.Branch} 6:{current_user.phone_no}7:{current_user.semester}")
        return jsonify({"response":"Credentials Found",
                        "and_id":current_user.and_id,
                        "name":current_user.name,
                        "USN":current_user.USN,
                        "email":current_user.email,
                        "password":current_user.password,
                        "branch":current_user.Branch,
                        "phone_no":current_user.phone_no,
                        "semester":current_user.semester
                        }), 200 
    except Exception as e:
        print(e)
        return jsonify({"response":"Internal Server Error"}),500
  
    
    
    
@pages.route('/update-user-profile',methods=['POST'])
@jwt_required()
def update_user_profile():
    """
    Used to update the user profile data.
    Inputs:
            1.name of the user, form variable name = name,
            2.USN of the user, form variable name = usn,
            3.email of the user, form variable name = email,
            4.Branch of the user, form variable name = Branch,
            5.phone number of the user,form variable name = phone no. 
    Outputs:
            200 for successful update.
            500 for any error.
    """
    from .dbmodels import Users
    from .Main import db
    try:
        current_user_id = get_jwt_identity()
        current_user=Users.query.filter_by(and_id=current_user_id).first()
        print("Current user:", current_user)
        if not current_user:
            return jsonify({"response": "User not found"}), 404

        data = request.get_json()
        print("Received data:", data)

        # Update only allowed fields
        current_user.name = data.get("name", current_user.name)
        current_user.Branch = data.get("branch", current_user.Branch)
        current_user.phone_no = data.get("phone_no", current_user.phone_no)
        current_user.semester = data.get("semester", current_user.semester)
        db.session.commit()
        return jsonify({"response": "User Profile Updated"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Internal Server Error"}), 500

