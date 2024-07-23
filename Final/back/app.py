from flask import Flask, request, jsonify
import os
from celery import Celery
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
from PIL import Image
import logging
from tkinter_app import RedisHandler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def make_celery(app):
    celery = Celery(app.import_name, backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

# Configuración del logger
redis_handler = RedisHandler()
redis_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
redis_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(redis_handler)
logger.setLevel(logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    file.save(filepath)
    task = classify_image.delay(filepath)
    return jsonify({"task_id": task.id}), 202

@app.route('/classify', methods=['POST'])
def classify():
    image_path = request.form['image_path']
    task = classify_image.delay(image_path)
    return jsonify({"task_id": task.id}), 202

@celery.task(name='app.classify_image')
def classify_image(filepath):
    logger.info(f"Processing image: {filepath}")
    
    try:
        model = tf.keras.models.load_model('simple_cnn_model.keras')  # Usar formato Keras
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return "Error loading model"

    try:
        img = Image.open(filepath)
        img = img.resize((150, 150))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = 'Pizza' if predictions[0] > 0.5 else 'Carne'
        
        logger.info(f"Predicted class: {predicted_class}")
        return predicted_class
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return "Error processing image"

@app.route('/result/<task_id>')
def get_result(task_id):
    task = classify_image.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result,
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
