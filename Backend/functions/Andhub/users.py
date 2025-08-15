"""
File used to store users related routes.

"""


# flask module imports.
from flask import Blueprint ,jsonify , request
from flask_jwt_extended import get_jwt_identity, jwt_required

from flask_cors import CORS
# other modules.



# project file imports.


from .auth import generate_and_id , generate_otp



# Bluerprint declaration.
users=Blueprint('Users',__name__)
CORS(users)


# Global dictionary used to store otps.
otps={}

@users.route('/confirm-email', methods=['POST'])
def email_confirmation():
    """
    Used to send an OTP to confirm the email. It calls the send_otp function from mail_handler.py.
    Inputs:
        * Email of the user, json variable name = email.
        * Name of the user, json variable name = name.
    Output:
        200 for success, 409 if email already present, 503 if mail fails
    """
    try:
        from .Main import db
        from .dbmodels import Users
        from .mail_handler import send_otp_email  # ✅ Make sure to import this

        data = request.get_json()
        email = data['email']
        name = data['name']

        # Check if email already exists in DB
        present = db.session.execute(db.select(Users).filter_by(email=email)).fetchone()
        if present:
            return jsonify({'response': "User with same email already present."}), 409

        # Generate and store OTP
        otp = generate_otp()
        otps[email] = otp

        # ✅ Call internal function (no HTTP, no CORS)
        success, message = send_otp_email(email=email, user_name=name, otp=otp)
        if not success:
            return jsonify({'response': message}), 503

        return jsonify({'otp': otp}), 200

    except Exception as e:
        return jsonify({"response": str(e)}), 500

       
    



@users.route('/register', methods=['POST'])
def register_user():
    """
    Used to register the user to the database. It compares the OTP sent by the system and the one received from frontend.
    Inputs:
        - name (string)
        - usn (string)
        - email (string)
        - password (string)
        - otp (int)
    Outputs:
        - 200: Success + sends welcome email
        - 401: OTP mismatch
        - 409: Email or USN already exists
        - 503: Mail failure
    """
    try:
        from .Main import db
        from .dbmodels import Users
        from .mail_handler import send_greeting_email  # ✅ Import the helper

        data = request.get_json()
        email = data['email']

        # Validate OTP
        if not int(data['otp']) == otps.get(email):
            return jsonify({"response": "Otp Does not match"}), 401

        and_identity = generate_and_id()
        user_name = data['name']
        usn = data['usn']
        password = data['password']
        user_type = 'USER'

        # Check if USN or email already exists
        if db.session.execute(db.select(Users).filter_by(USN=usn)).fetchone():
            return jsonify({'response': "User with same USN already present."}), 409
        if db.session.execute(db.select(Users).filter_by(email=email)).fetchone():
            return jsonify({'response': "User with same email already present."}), 409

        # Create and save new user
        user = Users(
            and_id=and_identity,
            name=user_name,
            USN=usn,
            user_type=user_type,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        # ✅ Call internal mail function (not via requests)
        success, msg = send_greeting_email(email=email, user_name=user_name)
        if not success:
            return jsonify({'response': msg}), 503

        return jsonify({"response": "Email Sent successfully."}), 200

    except Exception as e:
        print("Error during registration:", e)
        return jsonify({"response": str(e)}), 500






@users.route("/change-password",methods=["POST"])
@jwt_required
def change_password():
    """
    Used to change the password of the user.
    INPUT:
            1.user's new password, json variable name = new password.

    """
    try:
        from .dbmodels import Users
        user_id=get_jwt_identity()
        user_object=Users.query.filter_by(and_id=user_id).first()
        password=request.get_json()["new password"]

    except Exception as e:
        print("Errror at change password",e)
        return jsonify({"response":"Internal Server Error"}) ,500