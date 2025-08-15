"""
This file is used to Handle mail services of the website.

"""

# flask imports.
from os import name
from flask import Blueprint,request,jsonify
from flask_mail import Mail , Message
from flask_cors import CORS


# Defining the blue print.
mail_service=Blueprint('mail service',__name__)
CORS(mail_service)

and_mail=Mail()


def send_greeting_email(email, user_name):
    try:
        msg = Message(
            subject='Welcome to AND',
            sender='And team',
            recipients=[email]
        )
        msg.html = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome Page</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0f4f9; display: flex; justify-content: center; align-items: center; height: 100vh;">
                
                    <div style="width: 400px; background-color: #fff; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); overflow: hidden; text-align: center;">
                        
                        <!-- Header Section -->
                        <div style="background-color: #1560bd; color: white; padding: 20px; font-size: 20px; font-weight: bold;">
                            Welcome to Assignment and Notes Distribution Hub
                        </div>
                        
                        <!-- Body Section -->
                        <div style="padding: 20px; color: #333; line-height: 1.6;">
                            <p>Hello <strong>{user_name}</strong>,</p>
                            <p>We are thrilled to have you onboard! You can access all the resources on our website and are welcome to upload any resources as well</p>
                            <p style="margin-top: 20px;">
                                <a href="#" style="background-color: #F28C28; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; display: inline-block;">Get Started</a>
                            </p>
                        </div>
                        
                        <!-- Footer Section -->
                        <div style="background-color: #f7f9fc; border-top: 1px solid #ddd; padding: 10px; font-size: 12px; color: #777;">
                            <p>&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                            <a href="#" style="color: #0073e6; text-decoration: none; margin: 0 5px;">Privacy Policy</a> | 
                            <a href="#" style="color: #0073e6; text-decoration: none; margin: 0 5px;">Contact Support</a>
                        </div>
                        
                    </div>
                
                </body>
                </html>
                """.format(user_name=user_name)  # your full HTML here
        and_mail.send(msg)
        return True, "Email sent"
    except Exception as e:
        print("Error sending greeting email:", e)
        return False, str(e)
    
def send_otp_email(email, user_name, otp):
    try:
        msg = Message(
            subject='One Time Password for registration',
            sender='And team',
            recipients=[email]
        )
        msg.html = f"""
             <!DOCTYPE html>
             <html lang="en">
             <head>
             <meta charset="UTF-8">
             <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>OTP Code</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0f4f9; display: flex; justify-content: center; align-items: center; height: 100vh;">
                
                    <div style="width: 400px; background-color: #fff; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); overflow: hidden; text-align: center;">
                        
                        <!-- Header Section -->
                        <div style="background-color: #1560bd; color: white; padding: 20px; font-size: 20px; font-weight: bold;">
                            Your OTP Code
                        </div>
                        
                        <!-- Body Section -->
                        <div style="background-color: #1F75FE; padding: 20px; color: white; line-height: 1.6;">
                            <p>Mr/Ms <strong>{user_name}</strong>,</p>
                            <p>Thank you for using our service. Your One-Time Password (OTP) for verification is:</p>
                            <div style="font-size: 28px; font-weight: bold; color: #F28C28; border: 1px dashed #ff9900; display: inline-block; padding: 10px 20px; margin: 20px 0; background-color: white;">
                                {otp}
                            </div>
                            <p>Please use this code within the next 10 minutes. If you did not request this, please ignore this email or contact our support team immediately.</p>
                        </div>
                        
                        <!-- Footer Section -->
                        <div style="padding: 10px 20px; font-size: 14px; color: #555; line-height: 1.4; background-color: #1F75FE; color: white;">
                            Thank you,<br>
                            The <strong>AND Hub</strong> Team
                        </div>
                        
                        <!-- Bottom Section -->
                        <div style="background-color: #1F75FE; border-top: 1px solid #ddd; padding: 10px; font-size: 12px; color: white;">
                            <p>&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                            <a href="#" style="color: #FFD700; text-decoration: none; margin: 0 5px;">Privacy Policy</a> | 
                            <a href="#" style="color: #FFD700; text-decoration: none; margin: 0 5px;">Contact Support</a>
                        </div>
                        
                    </div>
                
                </body>
                </html>
                """  # same OTP email HTML you wrote
        and_mail.send(msg)
        return True, "OTP sent"
    except Exception as e:
        print("Error sending OTP email:", e)
        return False, str(e)
    
    
    
def send_forgot_password_otp(email, user_name, otp):
    try:
        msg = Message(
            subject='One Time Password for Password Reset',
            sender='And team',
            recipients=[email]
        )
        msg.html = f"""
             <!DOCTYPE html>
             <html lang="en">
             <head>
             <meta charset="UTF-8">
             <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>OTP Code</title>
                </head>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0f4f9; display: flex; justify-content: center; align-items: center; height: 100vh;">
                
                    <div style="width: 400px; background-color: #fff; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); overflow: hidden; text-align: center;">
                        
                        <!-- Header Section -->
                        <div style="background-color: #1560bd; color: white; padding: 20px; font-size: 20px; font-weight: bold;">
                            Password Reset OTP
                        </div>
                        
                        <!-- Body Section -->
                        <div style="background-color: #1F75FE; padding: 20px; color: white; line-height: 1.6;">
                            <p>Mr/Ms <strong>{user_name}</strong>,</p>
                            <p>We received a request to reset your password. Your One-Time Password (OTP) for verification is:</p>
                            <div style="font-size: 28px; font-weight: bold; color: #F28C28; border: 1px dashed #ff9900; display: inline-block; padding: 10px 20px; margin: 20px 0; background-color: white;">
                                {otp}
                            </div>
                            <p>Please use this code within the next 10 minutes to complete your password reset. If you did not request this, please ignore this email or contact our support team immediately.</p>
                        </div>
                        
                        <!-- Footer Section -->
                        <div style="padding: 10px 20px; font-size: 14px; color: #555; line-height: 1.4; background-color: #1F75FE; color: white;">
                            Thank you,<br>
                            The <strong>AND Hub</strong> Team
                        </div>
                        
                        <!-- Bottom Section -->
                        <div style="background-color: #1F75FE; border-top: 1px solid #ddd; padding: 10px; font-size: 12px; color: white;">
                            <p>&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                            <a href="#" style="color: #FFD700; text-decoration: none; margin: 0 5px;">Privacy Policy</a> | 
                            <a href="#" style="color: #FFD700; text-decoration: none; margin: 0 5px;">Contact Support</a>
                        </div>
                        
                    </div>
                
                </body>
                </html>
                """
        and_mail.send(msg)
        return True, "Password reset OTP sent"
    except Exception as e:
        print("Error sending password reset OTP:", e)
        return False, str(e)

    
