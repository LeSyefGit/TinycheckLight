import os, uuid, shutil, touch, sys,json
import subprocess as sp
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import desc
from flask_jwt_extended  import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from tinycheckweb.models import Capture, User
from tinycheckweb import db

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

            return jsonify(status=True, message="Upload perform successfully"), 200

class Analysis(object):

    def __init__(self, token):
        self.token = token 

    def start(self):
        """
            Start an analysis of the captured communication by lauching
            analysis.py with the capture token as a paramater.

            :return: dict containing the analysis status
        """

        if self.token is not None:
            # parent = "/".join(sys.path[0].split("/")[:-2])
            parent = current_app.root_path
            sp.Popen(
                [sys.executable, "{}/analysis/analysis.py".format(parent), "/tmp/{}".format(self.token)])
            
            return {"status": True,
                    "message": "Analysis started",
                    "token": self.token}
        else:
            return {"status": False,
                    "message": "Bad token provided",
                    "token": "null"}

    def get_report(self):
        
        """
            Generate a small json report of the analysis
            containing the alerts and the device properties.

            :return: dict containing the report or error message.
        """

        device, alerts = {}, {}

        # Getting device configuration.
        if os.path.isfile("/tmp/{}/assets/device.json".format(self.token)):
            with open("/tmp/{}/assets/device.json".format(self.token), "r") as f:
                device = json.load(f)

        # Getting alerts configuration.
        if os.path.isfile("/tmp/{}/assets/alerts.json".format(self.token)):
            with open("/tmp/{}/assets/alerts.json".format(self.token), "r") as f:
                alerts = json.load(f)

        if device != {} and alerts != {}:
            return {"alerts": alerts,
                    "device": device}
        else:
            return {"message": "No report yet"}



@capture.route('/start-analysis', methods=['POST'])
@jwt_required()
def start_analysis():
    user = User.query.filter_by(email=get_jwt_identity()).first()

    analyse_path = "/tmp/"

    if user :
        token = user.email.split('@')[0]

        #Delete a directory
        try:
            shutil.rmtree(analyse_path+token)
        except:
            pass
        # create different directory
        first = analyse_path+token+"/assets"
        os.makedirs(first)
        touch.touch([first+"/alerts.json",first+"/conns.json",first+"/whitelist.json"])
        
        capture = Capture.query.order_by(Capture.id.desc()).filter_by(user_id=user.id).first()

        upload_path = current_app.root_path+current_app.config["UPLOAD_FOLDER"]
        source_path = upload_path+capture.path
        new_filename = '/capture.pcap'
        dest_path = '/tmp/'+token + new_filename
        shutil.copyfile(source_path, dest_path)
        
        return jsonify(Analysis(token).start())