#import the necessary libraries
from flask import Flask, render_template, request, send_from_directory
import os
import uuid
from ffmpeg_utils import convert_video

app = Flask(__name__)
UPLOAD_FOLDER = 'app/uploads'  # folder to store the uploaded videos from the user
CONVERTED_FOLDER = 'app/converted' #folder to store the converted videos 

#if the upload folder does not exist, create it using os.makedirs
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#if the converted folder does not exist, create it using os.makedirs
if not os.path.exists(CONVERTED_FOLDER):
    os.makedirs(CONVERTED_FOLDER)

# serve the index page when the user access the root URL /
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html') # this will render the index.html file from the templates folder

@app.route('/convert', methods=['POST'])
def convert():
    if 'video' not in request.files:
        return "No file", 400
    
    # get the uploaded file and check if it has a filename
    file=request.files['video']
    if file.filename == '':
        return "No selected file", 400
    
    #retrive the file format from the form data and if it is not provided, default to mp4
    target_format =  request.form.get('format','mp4')
    if target_format not in ['mp4','avi','mkv','mov','webm']:
        return "Invalid format", 400

#generate a unique filename for the uploaded video
    unique_filename = str(uuid.uuid4())
    # set the input path for the uploaded video
    input_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    output_filename = f"{unique_filename}.{target_format}"

    #set the output path for the converted video
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    #save the uploaded file to the upload folder
    file.save(input_path)

# convert the video using the convert_video function from ffmpeg_utils
    try:
        convert_video(input_path, output_path)
        os.remove(input_path)
        return render_template("index.html", download_url=f"/converted/{output_filename}")
    except Exception as e:
        return f"Conversion failed: {e}", 500

#allow the user to download the converted video
@app.route('/converted/<path:unique_filename>', methods=['GET'])
def download_video(unique_filename):
    return send_from_directory(CONVERTED_FOLDER, unique_filename, as_attachment=True)
    
# run the flask application.
if __name__ == "__main__":
    app.run(debug=True)