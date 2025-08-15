"""
File is used to code the database models of the website.
*files stored in the upload folder will have their names changed to their and_id.



"""

# Flask Modules
from flask_login import UserMixin


import datetime
# Project Modules
from .Main import db


# Database tables

class Users(db.Model,UserMixin):
    """
    Database Model class , used to store user data .This class is combination of the database Model class and UserMixin class. 
    It is used to store user data and get the id for logging in purpose.

    """

    and_id=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(25),nullable=False)
    USN=db.Column(db.String(10),nullable=False)
    user_type=db.Column(db.String(10),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    #year=db.Column(db.(),nullable=True)
    Branch=db.Column(db.String(20),nullable=True)
    phone_no=db.Column(db.String(10),nullable=True)
    semester=db.Column(db.String(20),nullable=True)

    def to_dict(self):
        return {
            "and_id": self.and_id,
            "name": self.name,
            "USN": self.USN,
            "email": self.email,
            "password": self.password,
            "user_type": self.user_type,
            "branch": self.Branch,
            "phone_no": self.phone_no,
            "semester": self.semester,
        }

class MaterialMetadata(db.Model):
    __tablename__ = 'material_metadata'
    
    id = db.Column(db.Integer, primary_key=True)
    and_id = db.Column(db.String(100), db.ForeignKey('users.and_id'), nullable=False)
    
    semester = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    upload_type = db.Column(db.String(50), nullable=False)
    subject_code = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text)
    original_file_name = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.Text, nullable=False)
    # uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    subject_name = db.Column(db.String(60), nullable=True)
    description = db.Column(db.Text, nullable=True)
