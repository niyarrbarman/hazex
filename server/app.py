from flask import Flask, redirect, render_template, request
from utils import load_model, clear_dir, pred_read_image, mask_parse, placeMaskOnImg, Predict, area
from imports import np, plt
import os


model = load_model()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['OUTPUT_FOLDER'] = './static/output'

@app.route('/')
def index():
    clear_dir(app.config['UPLOAD_FOLDER'])
    clear_dir(app.config['OUTPUT_FOLDER'])
    return render_template('index.html')


@app.route('/run', methods=['POST'])
def image_upload():
    clear_dir(app.config['UPLOAD_FOLDER'])
    clear_dir(app.config['OUTPUT_FOLDER'])
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    # Get the full file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    # Save the file
    file.save(file_path)
    os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], 'input.png'))
    file_path = './static/uploads/input.png'

    return render_template('index.html')


def main():
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()