import os,datetime
import config
import numpy as np
import scipy.io.wavfile
from flask import Flask,request, redirect, url_for,session,flash
from flask.ext.session import Session
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from flask import render_template
from collections import OrderedDict


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
Bootstrap(app)
Session(app)
socketio = SocketIO(app, manage_session=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
def index(): pass

@app.route('/dashboard' , methods=['POST','GET'])
def dashboard():
	if request.method == 'POST':
		#file not present in request check
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		#check filename empty
		if file.filename == '':
			flash('No file selected')
			return redirect(request.url)
		#check filename allowed extensions
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if os.path.isdir(config.UPLOAD_FOLDER_FORM):
				try:
					os.makedirs(config.UPLOAD_FOLDER_FORM)
				except OSError as e:
					print
			file.save(os.path.join(config.UPLOAD_FOLDER_FORM,filename))
			flash('Upload done')
			return render_template('dashboard.html')
		else:
			flash('Upload files with .wav format')
			return redirect(request.url)
	return render_template('dashboard.html')

@socketio.on('connect')
def socketConnection():
	session['curren_session_audio'] = []


@socketio.on('disconnect', namespace='/disconnectstream')
def socketDisconnect():
	
	if not os.path.isdir(config.AUDIO_DIR):
		try:
			os.makedirs(config.AUDIO_DIR)

		except OSError as e:
			print e.message
	print 'writing file to : ' + config.AUDIO_DIR + "/"+ config.AUDIO_FILE + '.wav'
	scipy.io.wavfile.write(config.AUDIO_DIR + "/"+ config.AUDIO_FILE + '.wav', 
		config.FILE_WRITE_RATE , np.array(session['curren_session_audio']))

@socketio.on('listenaudio', namespace='/streamaudio')
def handle_audio_receiver(audio):
	session['curren_session_audio'] += OrderedDict(sorted(audio.items() , key=lambda  t:int(t[0]))).values()




