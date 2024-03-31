from flask import Flask, render_template,request,jsonify
from PIL import Image


app = Flask(__name__)
app = Flask(__name__, static_folder='assets')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def upload():
    return render_template('about.html')

@app.route('/services')
def results():
    return render_template('services.html')


@app.route('/upload', methods=['POST'])
def handle_image_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    print(file)
    image = Image.open(file.stream)
    print("seperator")
    print(image)
    
    prediction = "Disease Detected: DummyResponse"

    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True)
