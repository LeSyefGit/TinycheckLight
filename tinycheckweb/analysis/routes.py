import os, uuid
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended  import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from tinycheckweb.models import Capture, User
from tinycheckweb import db

analysis_bp = Blueprint('analysis',__name__)

ALLOWED_EXTENSIONS = {'pcap'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analysis_bp.route('/upload-pcap', methods=['POST'])
@jwt_required()
def start():
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

            #filename of the pcap file    
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_path, filename))

            source_path = upload_path+filename
            new_filename = str(uuid.uuid4())+'.pcap'
            dest_path = upload_path+ new_filename

            # rename the uploaded file in the destination to have 
            # a file with a unique identifier
            os.rename(source_path, dest_path)
            
            capture = Capture(path=new_filename, user_id=user.id)
            db.session.add(capture)
            db.session.commit()

            return jsonify(status=True, message="Upload perform successfully")
          