from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Profile(db.Model):
    email_id = db.Column(db.String(250), unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(250),  nullable=False)
    last_name=db.Column(db.String(250),  nullable=False)
    phone_number=db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, email_id, first_name, last_name, phone_number,password):
            self.email_id = email_id
            self.first_name = first_name
            self.last_name = last_name
            self.phone_number = phone_number
            self.password = password
            