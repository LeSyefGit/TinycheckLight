from flask import Blueprint, request, jsonify
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


