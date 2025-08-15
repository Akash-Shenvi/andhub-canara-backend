"""
This file contains authentication url endpoints and authentication settings.

"""

# Flask imports 

import flask_login as fl
from flask import Blueprint, jsonify, redirect ,request,abort, session ,render_template, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,verify_jwt_in_request

# Ohter imports
import random 
import uuid
import requests
import json
from datetime import timedelta


# Defining the blueprint
auth=Blueprint('auth',__name__)



#global Variables.
otps={}






# Project Fucntions.
def generate_and_id() -> str:
    """
    Used to generate 
    output:
    *returns 10 character unique id.
    """
    unique_id = uuid.uuid4()
    return str(unique_id)[0:10]
    





def generate_otp() ->int :
    """
    Used to generate otp 
    output:
    *returns the 6 digit otp
    """
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return int(otp)





@auth.route('/login',methods=["GET",'POST'])
def login():
    """
    Used to get login authorization and user object on the active users list.
    Inputs:
    1.User's email, json variable name= email.
    2.User's passowrd, json variable name = passowrd.

    Output:
    *returns-
                200 and ACCESS TOKEN, for successfull data found.
                401 , for invalid credentials.
                500 , for server side error.
    """
    from .dbmodels import Users
    try:
        if request.method=="GET":
                verify_jwt_in_request()
                current_user=get_jwt_identity()
                print("current user at login",current_user)
                if current_user:
                    return jsonify({'response':"Credentials Accepted."}) , 200 
                else:
                    return jsonify({'response':"User not logged in"}), 401
        user_data={}
        if request.method == 'POST': 
            user_data['email']=request.get_json()['email']
            user_data['password']=request.get_json()['password']
            print("1",user_data['email'],"2",user_data['password'])
            user=Users.query.filter_by(email=user_data['email']).first()
            if user:
                if user.password == user_data['password']:
                    print("session at 1",dict(session))
                    access_token=create_access_token(identity=user.and_id, expires_delta=timedelta(days=30*6))
                    return jsonify({'response':"Credentials Accepted.","accesstoken":access_token}) , 200          
                else:
                    return jsonify({'response':"Invalid Credentials"}) , 401
            else:
                print(user)
                print("user",request.form.get("username"),"password",user_data['password'])
                return jsonify({"response":"User Not present"}), 400
    except Exception as e:
        print("Error at login",f"{e}")
        return jsonify({"response":"Internal server Error"}),500
    




@auth.route('/forgot-password', methods=['POST', 'PUT'])
def forgot_password():
    from .dbmodels import Users
    from .Main import db
    from .mail_handler import send_forgot_password_otp
    global otps
    try:
        if request.method == 'POST':
            user_data = request.get_json()
            email = user_data['email']
            user = Users.query.filter_by(email=email).first()
            if user:
                user_email = user.email
                user_name = user.name
                otp = generate_otp()
                otps[user_email] = otp

                # Send Forgot Password OTP Email
                success, message = send_forgot_password_otp(user_email, user_name, otp)
                if success:
                    return jsonify({"response": "OTP generated and sent successfully"}), 200
                else:
                    return jsonify({"response": f"OTP generation succeeded but email failed: {message}"}), 500
            
            else:
                return jsonify({"response": "User Not Available"}), 400

        elif request.method == 'PUT':
            post_user_data = request.get_json()
            email_post = post_user_data["email"]
            otp_post = post_user_data["otp"]
            password = post_user_data['password']
            
            if email_post in otps and otps[email_post] == int(otp_post):
                del otps[email_post]
                user = Users.query.filter_by(email=email_post).first()
                user.password = password
                db.session.commit()
                return jsonify({"response": "Verification Complete. Password changed."}), 200
            
            elif email_post not in otps:
                return jsonify({"response": "OTP expired"}), 410
            
            else:
                return jsonify({"response": "OTP did not match"}), 401
        
        else:
            abort(405)

    except Exception as e:
        print("Error in forgot password:", e)
        return jsonify({"response": "Internal Server Error"}), 500





@auth.route("/admin/users", methods=["GET"])
@jwt_required()
def get_users():
    
    from .dbmodels import Users
    current_user = get_jwt_identity()
    user= Users.query.filter_by(and_id=current_user).first()
    if user.user_type not in ['DEVELOPER']:
        return jsonify({'error': 'Please Contact Developer to Become maintainer to upload'}), 403
    users = Users.query.all()
    return jsonify({
        "users": [u.to_dict() for u in users]
    })
    
@auth.route("/admin/users/<string:and_id>", methods=["PUT"])
@jwt_required()
def update_user(and_id):
    from .dbmodels import Users
    from .Main import db
    data = request.get_json()
    current_user = get_jwt_identity()
    users=Users.query.filter_by(and_id=current_user).first()
    user = Users.query.filter_by(and_id=and_id).first()
    if users.user_type not in ['DEVELOPER']:
        return jsonify({'error': 'Please Contact Developer to Become maintainer to upload'}), 403
    if not user:
        return jsonify({"error": "User not found"}), 404

    editable_fields = ["name", "USN", "email", "password", "user_type", "branch", "phone_no", "semester"]

    for field in editable_fields:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

