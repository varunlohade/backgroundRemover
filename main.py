import rembg
import numpy as np
from flask import Flask, request, jsonify, send_file
from PIL import Image
from io import BytesIO
from random import randint


app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/removeBackground", methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image_file = request.files['image']
    image = Image.open(image_file)

    image_np = np.array(image)

    output = rembg.remove(image_np)

    output_image = Image.fromarray(output)

    passport_size = (600, 600)  # 2x2 inches at 300dpi
    output_image = output_image.resize(passport_size)

    output_image = output_image.convert('RGBA')

    background_image = Image.new('RGBA', passport_size, (0, 255, 0, 255))

    background_image.paste(output_image, (0, 0), output_image)

    # Save the output image as a BytesIO object
    output_bytes = BytesIO()
    background_image.save(output_bytes, format='PNG')
    output_bytes.seek(0)

    return send_file(output_bytes, mimetype='image/png')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
