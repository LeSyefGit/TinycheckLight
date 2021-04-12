import os, uuid, shutil,sys,json
import subprocess as sp
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import desc
from flask_jwt_extended  import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from tinycheckweb.models import Capture, User
from tinycheckweb import db
from .analysis import Analysis

capture = Blueprint('capture',__name__)

ALLOWED_EXTENSIONS = {'pcap'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@capture.route('/upload-pcap', methods=['POST'])
@jwt_required()
def upload_pcap():
    user = User.query.filter_by(email=get_jwt_identity()).first()

    if user :
        # check if the post request has the file part
        if 'capture' not in request.files:
            return jsonify(status=False,error="No file part")

        file = request.files['capture']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
           return jsonify(status=False, error="No selected file")

        if file and allowed_file(file.filename):
            # Path where we will store our file
            upload_path = current_app.root_path+current_app.config["UPLOAD_FOLDER"]

            # Get the filename of the uploaded file    
            filename = secure_filename(file.filename)
            # Save the file in our server
            file.save(os.path.join(upload_path, filename))

            # Rename the uploaded file with the unique identifier
            source_path = upload_path+filename
            new_name = str(uuid.uuid4())+'.pcap'
            dest_path = upload_path+ new_name
            os.rename(source_path, dest_path)
            
            # Save the file within the database 
            capture = Capture(path=new_name, user_id=user.id)
            db.session.add(capture)
            db.session.commit()

            return jsonify(status=True, message="Upload perform successfully"), 200


@capture.route('/start-analysis', methods=['POST'])
@jwt_required()
def start_analysis():
    user = User.query.filter_by(email=get_jwt_identity()).first()

    # Path where we will do our analyse
    analyse_path = "/tmp/"

    if user :
        # Get the first part of the name of user to make his username
        token = user.email.split('@')[0]

        #Delete a directory corresponding to the username of user if exist
        try:
            shutil.rmtree(analyse_path+token)
        except:
            pass

        # Create arborescence for analysing
        directory = analyse_path+token+"/assets"
        os.makedirs(directory)
        
        # Get the latest pcap file of user to analyse
        capture = Capture.query.order_by(Capture.id.desc()).filter_by(user_id=user.id).first()

        if capture :
            upload_path = current_app.root_path+current_app.config["UPLOAD_FOLDER"]

            # Copy the latest uploaded pcap file of user into /tmp for analysing
            # and rename it in capture.pcap
            source_path = upload_path+capture.path
            new_filename = '/capture.pcap'
            dest_path = '/tmp/'+token + new_filename
            shutil.copyfile(source_path, dest_path)
            
            return jsonify(Analysis(token).start())
        else:
            return jsonify(message="No pcap file found ! Try to upload one")

@capture.route('/get-report', methods=['GET'])
@jwt_required()
def get_report():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    token = user.email.split('@')[0]

    analyse_path = "/tmp/"+token

    if user and os.path.exists(analyse_path) :
        token = user.email.split('@')[0]
        return jsonify(Analysis(token).get_report())
    else:
        return jsonify(message="No report found ! Try to make analysis")