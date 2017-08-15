import os
from flask import Flask, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = 'tmp/uploads'
ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'm4p', '3gp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			response = make_response(jsonify({'error': 'request does not have a file', 'result':'none'}),400)
			response.headers['Content-Type'] = 'application/json'
			return response
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			response = make_response(jsonify({'error': 'file must have a name', 'result': 'none'}),400)
			response.headers['Content-Type'] = 'application/json'
			return response
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filepath)
			return process_file(filepath)

		response = make_response(jsonify({'error': 'internal server error', 'result':'none'}),500)
		response.headers['Content-Type'] = 'application/json'
		return response

def process_file(filepath):
	accent = analyze_accent(filepath)
	# os.remove(filepath)
	response = make_response(jsonify({'result':accent, 'error':'none'}),200)
	response.headers['Content-Type'] = 'application/json'
	return response

def analyze_accent(filepath):
	# TODO: implement actual analysis
	return 'To Be Implemented'

if __name__ == '__main__':
	app.run(debug=True)