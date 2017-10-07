import accent_analyzer as analyzer
import boto3
import os

def lambda_handler(event, context):
	print event
	print context
	
	s3_filename = ''
	
	try:
		s3_filename = event['s3_filename']
	except:
		raise Exception('s3_filename not found')
	
	return process_file(s3_filename)

def process_file(s3_filename):
	download_location = "/tmp/"+s3_filename
	try:
		download_file(s3_filename, download_location)
	except Exception as e:
		print e
		body = {'error': 'internal server error', 'result':'none'}
		headers = {'Content-Type': 'application/json'}
		return make_response(headers, body, 500)

	accent = analyze_accent(download_location)

	body = {'error': 'none', 'result': accent}
	headers = {'Content-Type': 'application/json'}
	# response.headers['Content-Type'] = 'application/json'
	return make_response(headers, body, 200)

def download_file(s3_filename, download_location):
	s3 = boto3.client('s3')
	s3.download_file("accentanalyzer-userfiles-mobilehub-545605178", "uploads/"+s3_filename, download_location)

def analyze_accent(filepath):
	relative_filepath = './{0}'.format(filepath)
	results = analyzer.main(filepath)
	return str(results)

def make_response(headers, body, status_code):
	response = {}
	response['headers'] = headers
	response['statusCode'] = status_code
	response['body'] = body
	response['isBase64Encoded'] = False

	return response