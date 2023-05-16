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
    image_path = os.path.join('draw_images', 'drawing.png')

    with open(image_path, 'wb') as f:
        f.write(image_data)

    # Adjust image dimensions
    adjusted_image_path = adjust_image_dimensions(image_path)

    return 'Saved'


def adjust_image_dimensions(image_path):
    # Open the image
    image = Image.open(image_path)

    # Get the original width and height
    original_width, original_height = image.size

    # Calculate the new dimensions that are multiples of 64
    new_width = (original_width // 64) * 64
    new_height = (original_height // 64) * 64

    # Resize the image using the new dimensions
    resized_image = image.resize((new_width, new_height))

    # Save the resized image with a new filename
    adjusted_image_path = os.path.splitext(image_path)[0] + '_adjusted.png'
    resized_image.save(adjusted_image_path)

    return adjusted_image_path

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)