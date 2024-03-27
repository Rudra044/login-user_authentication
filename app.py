from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db , Profile
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail,Message
from urllib.parse import unquote_plus, quote_plus
from config import Config
from util.utils import add_user, del_user , commit_changes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail=Mail(app)
            

@app.route("/register",methods=['POST'])
def create_user():
     data = request.json
     email_id = data.get('email_id')
     first_name = data.get('first_name')
     last_name= data.get('last_name')
     phone_number=data.get('phone_number')
     password = data.get('password')
     if email_id and first_name and last_name and phone_number and password:
        if Profile.query.filter_by(email_id=email_id).first():
            return jsonify({'error': 'User with this email or username already exists'})
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = add_user(email_id, first_name, last_name, phone_number, hashed_password)
        return jsonify({'message': 'User created successfully'})
     else:
        return jsonify({'error': 'All fields need to be provided'})
     

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email_id=data.get('email_id')
    user = Profile.query.filter_by(email_id=email_id).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email_id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid email or password'})
    

@app.route('/delete',methods=['DELETE'])
@jwt_required()
def delete_user():
    email_id = get_jwt_identity()
    user = Profile.query.filter_by(email_id=email_id).first()
    if user:
        del_user(user)
        return jsonify({'message': 'data deleted'})
    else:
        return jsonify({'error': 'Username are required'})
    

@app.route('/update',methods=['PATCH'])
@jwt_required()
def update_phone():
    email_id = get_jwt_identity()
    user = Profile.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    data = request.json
    phone_number=data.get('phone_number')
    first_name = data.get('first_name')
    last_name= data.get('last_name')
    if phone_number:
        user.phone_number = phone_number
        return jsonify({'message': 'Phone number updated successfully'})
    if first_name:
        user.first_name = first_name
        return jsonify({'message': 'first_name updated successfully'})
    if last_name:
       user.last_name = last_name
       return jsonify({'message': 'last_name updated successfully'})
    commit_changes()
    return jsonify({'message': 'invalid input'})

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    email_id = get_jwt_identity()
    users = Profile.query.all()
    return jsonify(([user.json() for user in users]))


@app.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    email_id = get_jwt_identity()
    data = request.json
    password = data.get('password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    
    user = Profile.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'User not found'})

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Incorrect password'})

    if not new_password:
        return jsonify({'message': 'New password not provided'})
    if not confirm_new_password:
        return jsonify({'message': 'Confirm_New password not provided'})
    if confirm_new_password != new_password:
        return jsonify({'message': 'Confirm_New password and new password field not match'})

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    commit_changes()

    return jsonify({'message': 'Password changed successfully'})


@app.route('/forget_password', methods=['POST'])
@jwt_required()
def forget_password():
    email_id = get_jwt_identity()
    data = request.json
    email_id=data.get('email_id')
    user = Profile.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    else:  
         encoded_email_id = quote_plus(email_id) 
         reset_link = f'http://127.0.0.1:5000/reset_password/{encoded_email_id}'
         msg = Message( 
                'Hello', 
                sender ='',
                recipients = [email_id]) 
         msg.body =  f'Hello,\n\nYour reset link is/ {reset_link}'
         mail.send(msg) 

         return jsonify({'message': 'The Mail is Send.'}) 


@app.route('/reset_password/<encoded_email_id>/<reset_token>', methods=['POST'])
def reset_password(encoded_email_id, reset_token):
    

    email_id = unquote_plus(encoded_email_id)  
    data = request.json
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
   
    user = Profile.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'Invalid email ID'})
    if confirm_new_password != new_password:
        return jsonify({'message': 'Confirm_New password and new password field not match'})

    
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    commit_changes()
    
    return jsonify({'message': 'Password reset successfully'})
        
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)