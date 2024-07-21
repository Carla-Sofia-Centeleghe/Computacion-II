import tensorflow as tf
import numpy as np
from PIL import Image

def classify_image(filepath):
    model = tf.keras.models.load_model('simple_cnn_model.h5')
    
    img = Image.open(filepath)
    img = img.resize((150, 150))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = 'Pizza' if predictions[0] > 0.5 else 'Carne'
    return predicted_class

print(classify_image('/home/carla/Documentos/GitHub/Computacion-II/Final/back/train_dir/carne/27415.jpg'))
