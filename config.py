import os,datetime,logging,logging.handlers,logging.config

UPLOAD_FOLDER = "/var/appaudio/"
UPLOAD_FOLDER_FORM = "/var/appaudio_form/"
ALLOWED_EXTENSIONS= set(['wav'])
FILE_WRITE_RATE = 44100
AUDIO_DIR = os.path.join(UPLOAD_FOLDER, datetime.datetime.now().strftime('%Y-%m-%d'))
AUDIO_FILE = os.path.join("", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))


#logging 
logging.config.fileConfig('log.conf',disable_existing_loggers =0)