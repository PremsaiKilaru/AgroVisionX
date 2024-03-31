from flask import Flask, render_template,request,jsonify
from PIL import Image
import os
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index



app = Flask(__name__)
app = Flask(__name__, static_folder='assets')
@app.route('/')
def home():
    return render_template('index.html',title="Disease Name",description="About Disease",prevent="Prevention Tips",supplement_name="Pesticide Name")

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
    image = request.files['file']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    print(image)
    filename = image.filename
    file_path = os.path.join('assets/uploads', filename)
    image.save(file_path)
    print(file_path)
    pred = prediction(file_path)
    title = disease_info['disease_name'][pred]
    description =disease_info['description'][pred]
    prevent = disease_info['Possible Steps'][pred]
    image_url = disease_info['image_url'][pred]
    supplement_name = supplement_info['supplement name'][pred]
    supplement_image_url = supplement_info['supplement image'][pred]
    supplement_buy_link = supplement_info['buy link'][pred]
    return render_template('index.html',title=title,description=description,prevent=prevent,supplement_name=supplement_name)


if __name__ == '__main__':
    app.run(debug=True)
