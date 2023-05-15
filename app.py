from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import re, base64, os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data_url = request.values['data']
    image_data = re.sub('^data:image/.+;base64,', '', data_url)
    image_data = base64.b64decode(image_data)
    image_path = os.path.join('images', 'drawing.png')

    with open(image_path, 'wb') as f:
        f.write(image_data)

    return 'Saved'

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)