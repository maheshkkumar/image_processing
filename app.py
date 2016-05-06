# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import image_processing
import os
from werkzeug import secure_filename
from gtts import gTTS
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPEG', 'JPG', 'PNG'])

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/result', methods=['POST'])
def result():
	image_file = request.files['file']
	if image_file and allowed_file(image_file.filename):
   		filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_name = image_processing.ImageProcessing(filename)
        description, tags = image_name.get_image_description()
        image = UPLOAD_FOLDER+"/"+filename
        with open('lifelog.txt', 'a') as file:
            file.write(description+".\n")
            file.close()
        return render_template('form_action.html', description=description, tags=tags, image=image)

@app.route('/audio', methods=['GET', 'POST'])
def audio():
    with open('lifelog.txt', 'r') as content_file:
        content = content_file.read()
    tts = gTTS(text=content, lang='en')
    tts.save('static/lifelog.mp3')   
    return render_template('audio.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Run the app :)
if __name__ == '__main__':
	app.run(debug = True)