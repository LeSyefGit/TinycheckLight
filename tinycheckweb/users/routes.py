from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from tinycheckweb import db, bcrypt
from tinycheckweb.models import User

users = Blueprint('users', __name__)

@users.route("/register", methods=['POST'])
def register():
    if request.is_json :
        email = request.json['email']
        hashed_password = bcrypt.generate_password_hash(request.json['password']).decode("utf-8")

        # Check if the user already exist
        test = User.query.filter_by(email=email).first()
        if test :
            return jsonify(message="That email already exist !"), 409
        else:
            user = User(email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify(message="Successfull registration. Perform a login to get access token"), 201

    return jsonify(message="Bad request"), 400

@users.route("/login", methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
        
        # Check if user already exist
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password,password) :
            access_token = create_access_token(identity=user.email)
            return jsonify(message="Login succeeded !", access_token=access_token), 200
        return jsonify(message="Bad email or password !"), 401
    return jsonify(message="Bad request !"), 401

@users.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
