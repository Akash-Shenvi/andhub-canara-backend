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

def made_user(email,user_name):
    try:
        msg= Message(
            subject='You Are Now A User',
            sender='And team',
            recipients=[email]
        )
        msg.html="""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Update on Your AND Hub Account</title>
    <style type="text/css">
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        @media screen and (max-width: 600px) {{
            .email-container {{
                width: 100% !important;
                margin: auto !important;
            }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0 !important; background-color: #1a1a2e;">

    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        An update on your account privileges on AND Hub.
    </div>

    <center style="width: 100%; background-color: #1a1a2e;">
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
            <tr>
                <td valign="top" style="padding: 20px 0;">
                    <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: auto; background-color: #2c3e50; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" class="email-container">
                        
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #1a1a2e; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                                <h1 style="margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: bold; color: #f7b731;">Maintainer Access Revoked</h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px; text-align: left; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #e0e0e0;">
                                <p style="margin: 0 0 20px 0;">Hello <strong>{user_name}</strong>,</p>
                                <p style="margin: 0 0 20px 0;">This is to inform you that your maintainer privileges on the AND Hub have been revoked. You will no longer have access to the admin routes, and you will not be able to upload, edit, or delete materials.</p>
                                <p style="margin: 0 0 30px 0;">Your account has been returned to standard user access, which allows you to browse and download all community resources. If you believe this is an error or have any questions, please don't hesitate to contact our support team.</p>
                                
                                <!-- CTA Button -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td align="center">
                                            <div>
                                                <!--[if mso]>
                                                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="#" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="10%" strokecolor="#f7b731" fillcolor="#f7b731">
                                                    <w:anchorlock/>
                                                    <center style="color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;">Go to Dashboard</center>
                                                </v:roundrect>
                                                <![endif]-->
                                                <a href="https://andhub-canara.web.app" style="background-color: #f7b731; border: 1px solid #f7b731; border-radius: 5px; color: #ffffff; display: inline-block; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; font-weight: bold; line-height: 40px; text-align: center; text-decoration: none; width: 200px; -webkit-text-size-adjust:none; mso-hide:all;">Go to Dashboard</a>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 30px; text-align: center; background-color: #1a1a2e; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                                <p style="margin: 0; font-size: 12px; color: #a9b4c2;">&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                                <p style="margin: 10px 0 0 0; font-size: 12px;">
                                    <a href="https://andhub-canara.web.app/privacy" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Privacy Policy</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/about" style="color: #f7b731; text-decoration: none; margin: 0 5px;">About</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/contact" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Contact Support</a>
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>

        
        """.format(user_name=user_name)
        and_mail.send(msg)
        return True,"Email sent"
    except Exception as e:
        print("Error sending user email:",e)
        return False,str(e)

def made_maintainer(email,user_name):
    try:
        msg = Message(
            subject='You Are Now A Maintainer',
            sender='And team',
            recipients=[email]
        )
        msg.html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>You're a Maintainer at AND Hub</title>
    <style type="text/css">
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        @media screen and (max-width: 600px) {{
            .email-container {{
                width: 100% !important;
                margin: auto !important;
            }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0 !important; background-color: #1a1a2e;">

    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        You have been granted maintainer access on AND Hub.
    </div>

    <center style="width: 100%; background-color: #1a1a2e;">
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
            <tr>
                <td valign="top" style="padding: 20px 0;">
                    <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: auto; background-color: #2c3e50; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" class="email-container">
                        
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #1a1a2e; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                                <h1 style="margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: bold; color: #f7b731;">New Maintainer Role Assigned</h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px; text-align: left; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #e0e0e0;">
                                <p style="margin: 0 0 20px 0;">Hello <strong>{user_name}</strong>,</p>
                                <p style="margin: 0 0 20px 0;">Congratulations! You have been granted maintainer privileges on the AND Hub. Your role is crucial to keeping our community's resources organized and up-to-date.</p>
                                <p style="margin: 0 0 30px 0;">With your new access, you can now manage the platform's content. This includes accessing the admin routes to upload new materials, edit the names and details of existing resources, and delete materials when necessary. We trust you to help us maintain a high-quality resource library for everyone.</p>
                                
                                <!-- CTA Button -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td align="center">
                                            <div>
                                                <!--[if mso]>
                                                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="#" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="10%" strokecolor="#f7b731" fillcolor="#f7b731">
                                                    <w:anchorlock/>
                                                    <center style="color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;">Go to Admin</center>
                                                </v:roundrect>
                                                <![endif]-->
                                                <a href="https://andhub-canara.web.app/admin" style="background-color: #f7b731; border: 1px solid #f7b731; border-radius: 5px; color: #ffffff; display: inline-block; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; font-weight: bold; line-height: 40px; text-align: center; text-decoration: none; width: 200px; -webkit-text-size-adjust:none; mso-hide:all;">Go to Admin</a>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 30px; text-align: center; background-color: #1a1a2e; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                                <p style="margin: 0; font-size: 12px; color: #a9b4c2;">&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                                <p style="margin: 10px 0 0 0; font-size: 12px;">
                                    <a href="https://andhub-canara.web.app/privacy" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Privacy Policy</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/about" style="color: #f7b731; text-decoration: none; margin: 0 5px;">About</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/contact" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Contact Support</a>
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>

        
        """.format(user_name=user_name)
        and_mail.send(msg)
        return True, "Email sent"
    except Exception as e:
        print("Error sending maintainer email:", e)
        return False, str(e)
                


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
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Welcome to AND Hub</title>
    <style type="text/css">
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        @media screen and (max-width: 600px) {{
            .email-container {{
                width: 100% !important;
                margin: auto !important;
            }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0 !important; background-color: #1a1a2e;">

    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        We're thrilled to have you onboard!
    </div>

    <center style="width: 100%; background-color: #1a1a2e;">
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
            <tr>
                <td valign="top" style="padding: 20px 0;">
                    <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: auto; background-color: #2c3e50; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" class="email-container">
                        
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #1a1a2e; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                                <h1 style="margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: bold; color: #f7b731;">Welcome to AND Hub</h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px; text-align: left; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #e0e0e0;">
                                <p style="margin: 0 0 20px 0;">Hello <strong>{user_name}</strong>,</p>
                                <p style="margin: 0 0 20px 0;">We are thrilled to have you onboard! You can access all the resources on our website and are welcome to upload any resources as well.</p>
                                <p style="margin: 0 0 30px 0;">Our platform is a comprehensive hub for all your academic needs, including notes, question banks, and placement preparation materials. Feel free to explore and distribute study materials to help the community grow.</p>
                                
                                <!-- CTA Button -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                    <tr>
                                        <td align="center">
                                            <div>
                                                <!--[if mso]>
                                                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="#" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="10%" strokecolor="#f7b731" fillcolor="#f7b731">
                                                    <w:anchorlock/>
                                                    <center style="color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;">Get Started</center>
                                                </v:roundrect>
                                                <![endif]-->
                                                <a href="https://andhub-canara.web.app" style="background-color: #f7b731; border: 1px solid #f7b731; border-radius: 5px; color: #ffffff; display: inline-block; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; font-weight: bold; line-height: 40px; text-align: center; text-decoration: none; width: 200px; -webkit-text-size-adjust:none; mso-hide:all;">Get Started</a>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 30px; text-align: center; background-color: #1a1a2e; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                                <p style="margin: 0; font-size: 12px; color: #a9b4c2;">&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                                <p style="margin: 10px 0 0 0; font-size: 12px;">
                                    <a href="https://andhub-canara.web.app/privacy" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Privacy Policy</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/about" style="color: #f7b731; text-decoration: none; margin: 0 5px;">About</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/contact" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Contact Support</a>
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </center>
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
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Your One-Time Password</title>
    <style type="text/css">
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        @media screen and (max-width: 600px) {{
            .email-container {{
                width: 100% !important;
                margin: auto !important;
            }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0 !important; background-color: #1a1a2e;">

    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        Here is your one-time password to complete your request.
    </div>

    <center style="width: 100%; background-color: #1a1a2e;">
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
            <tr>
                <td valign="top" style="padding: 20px 0;">
                    <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: auto; background-color: #2c3e50; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" class="email-container">
                        
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #1a1a2e; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                                <h1 style="margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: bold; color: #f7b731;">Your OTP Code</h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px; text-align: left; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #e0e0e0;">
                                <p style="margin: 0 0 20px 0;">Mr/Ms <strong>{user_name}</strong>,</p>
                                <p style="margin: 0 0 20px 0;">Thank you for using our service. Your One-Time Password (OTP) for verification is:</p>
                                
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <div style="background-color: #1a1a2e; border: 1px dashed #f7b731; padding: 20px; border-radius: 8px;">
                                                <span style="font-family: 'Courier New', Courier, monospace; font-size: 32px; font-weight: bold; color: #f7b731; letter-spacing: 4px; display: inline-block;">
                                                    {otp}
                                                </span>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 0;">Please use this code within the next 10 minutes. If you did not request this, please ignore this email or contact our support team immediately.</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 30px; text-align: center; background-color: #1a1a2e; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                                <p style="margin: 0 0 10px 0; font-size: 14px; color: #a9b4c2;"><span style="color: #f7b731;">Thank you,</span><br>The <strong style="color: #f7b731;">AND Hub</strong> Team</p>
                                <p style="margin: 0; font-size: 12px; color: #a9b4c2;">&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                                <p style="margin: 10px 0 0 0; font-size: 12px;">
                                    <a href="https://andhub-canara.web.app/privacy" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Privacy Policy</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/about" style="color: #f7b731; text-decoration: none; margin: 0 5px;">About</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/contact" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Contact Support</a>
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </center>
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
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Your One-Time Password</title>
    <style type="text/css">
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        @media screen and (max-width: 600px) {{
            .email-container {{
                width: 100% !important;
                margin: auto !important;
            }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0 !important; background-color: #1a1a2e;">

    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        Here is your one-time password to complete your request.
    </div>

    <center style="width: 100%; background-color: #1a1a2e;">
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
            <tr>
                <td valign="top" style="padding: 20px 0;">
                    <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; margin: auto; background-color: #2c3e50; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" class="email-container">
                        
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #1a1a2e; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                                <h1 style="margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: bold; color: #f7b731;">WELCOME TO AND HUB</h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px; text-align: left; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #e0e0e0;">
                                <p style="margin: 0 0 20px 0;">Hi <strong>{user_name}</strong>,</p>
                                <p style="margin: 0 0 20px 0;">We received a request to reset your password. Please use the One-Time Password (OTP) below to proceed. The code is valid for 10 minutes.</p>
                                
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <div style="background-color: #1a1a2e; border: 1px dashed #f7b731; padding: 20px; border-radius: 8px;">
                                                <span style="font-family: 'Courier New', Courier, monospace; font-size: 32px; font-weight: bold; color: #f7b731; letter-spacing: 4px; display: inline-block;">
                                                    {otp}
                                                </span>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 0;">If you did not request a password reset, please ignore this email or contact our support team if you have any concerns.</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 30px; text-align: center; background-color: #1a1a2e; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                                <p style="margin: 0 0 10px 0; font-size: 14px; color: #a9b4c2;"><span style="color: #f7b731;">Thank you,</span><br>The <strong style="color: #f7b731;">AND Hub</strong> Team</p>
                                <p style="margin: 0; font-size: 12px; color: #a9b4c2;">&copy; 2025 <strong>AND Hub</strong>. All rights reserved.</p>
                                <p style="margin: 10px 0 0 0; font-size: 12px;">
                                    <a href="https://andhub-canara.web.app/privacy" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Privacy Policy</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/about" style="color: #f7b731; text-decoration: none; margin: 0 5px;">About</a>
                                    <span style="color: #a9b4c2;">|</span>
                                    <a href="https://andhub-canara.web.app/contact" style="color: #f7b731; text-decoration: none; margin: 0 5px;">Contact Support</a>
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>

                """
        and_mail.send(msg)
        return True, "Password reset OTP sent"
    except Exception as e:
        print("Error sending password reset OTP:", e)
        return False, str(e)

    
