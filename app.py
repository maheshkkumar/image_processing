# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import image_processing

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/result/', methods=['POST'])
def result():
    image=request.form['url']
    image_name = image_processing.ImageProcessing(image)
    description, tags = image_name.get_image_description()
    return render_template('form_action.html', description=description, tags=tags, image=image)

# Run the app :)
if __name__ == '__main__':
	app.run(debug = True)