from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)

# AWS S3 Configuration
S3_BUCKET = 'flaskapp-bucket-13'  # Replace with your actual S3 bucket name
s3 = boto3.client('s3')  # Ensure IAM role or AWS credentials are correctly configured

@app.route('/')
def index():
    # Serve the HTML front-end
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error("No file selected")
        return jsonify({"error": "No file selected"}), 400

    try:
        app.logger.info(f"Uploading file: {file.filename}")
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        app.logger.info(f"File {file.filename} uploaded successfully")
        return jsonify({"message": f"File '{file.filename}' uploaded successfully"})
    except Exception as e:
        app.logger.error(f"Error during upload: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/list-files', methods=['GET'])
def list_files():
    try:
        objects = s3.list_objects_v2(Bucket=S3_BUCKET).get('Contents', [])
        files = [obj['Key'] for obj in objects]
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
