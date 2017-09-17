import os
from flask import Flask, request, redirect, url_for, make_response, jsonify
import boto3
import Training_Tester as analyzer

UPLOAD_FOLDER = 'tmp/uploads'
ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'm4p', '3gp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def process():
	if request.method == 'POST':
		s3_filename = request.form['s3_filename']

		log(s3_filename)

		return process_file(s3_filename)

def process_file(s3_filename):
	download_location = "tmp/"+s3_filename
	log(download_location)
	try:
		download_file(s3_filename, download_location)
	except Exception as e:
		print e
		response = make_response(jsonify({'error': 'internal server error', 'result':'none'}),500)
		response.headers['Content-Type'] = 'application/json'
		return response

	accent = analyze_accent(download_location)
	os.remove(download_location)

	response = make_response(jsonify({'error': 'none', 'result': accent}),200)
	response.headers['Content-Type'] = 'application/json'
	return response

def download_file(s3_filename, download_location):
	s3 = boto3.client('s3')
	s3.download_file("accentanalyzer-userfiles-mobilehub-545605178", "uploads/"+s3_filename, download_location)
	

def analyze_accent(filepath):
	# TODO: implement actual analysis
	log(filepath)
	relative_filepath = './{0}'.format(filepath)
	results = analyzer.main(filepath)
	return results

def log(msg):
	print msg

if __name__ == '__main__':
	app.run(debug=True)