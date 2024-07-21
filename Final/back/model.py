import zipfile
import os
import matplotlib.pyplot as plt
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


import requests
import zipfile
import io

def download_and_extract_data():
    url = "https://storage.googleapis.com/ztm_tf_course/food_vision/pizza_steak.zip"  # URL del archivo ZIP de comida a descargar
    response = requests.get(url) # Descargar el archivo ZIP desde la URL
    zip_ref = zipfile.ZipFile(io.BytesIO(response.content))  # Abrir el archivo ZIP descargado como un objeto ZipFile
    zip_ref.extractall() # Extraer todos los archivos del ZIP al directorio actual
    zip_ref.close()

download_and_extract_data() # Llamar a la función para descargar y extraer los datos


# Función principal
def AI():
    # Cargar y preprocesar los datos
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    train_dir = 'pizza_steak/train'
    test_dir = 'pizza_steak/test'

    train_batch = train_datagen.flow_from_directory(
        train_dir,
        target_size=(64, 64),  # Reducir el tamaño de las imágenes de entrada
        batch_size=32,
        class_mode='binary'
    )

    test_batch = test_datagen.flow_from_directory(
        test_dir,
        target_size=(64, 64),  # Reducir el tamaño de las imágenes de entrada
        batch_size=32,
        class_mode='binary'
    )

    # Definir el modelo
    model = Sequential([
        Input(shape=(64, 64, 3)), 
        Conv2D(16, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
   

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    model.summary()

    # Entrenar el modelo
    model.fit(
        train_batch,
        steps_per_epoch=len(train_batch),
        epochs=10,
        validation_data=test_batch,
        validation_steps=len(test_batch)
    )

    # Guardar el modelo
    model.save('optimized_model.h5')

    # Evaluar modelo con conjunto de prueba
    model.evaluate(test_batch)
    
    img = plt.imread('pizza_steak/test/pizza/1180273.jpg')
    img = img / 255.
    img_resized = tf.image.resize(img, (224, 224))
    img_expanded = tf.expand_dims(img_resized, axis=0)
    y_pred = model.predict(img_expanded)
    y_pred = tf.squeeze(y_pred)
    y_pred = tf.round(y_pred)
    print(f'La predicción para la imagen de pizza es: {y_pred}')

    # Definir clases
    class_labels = ['Steak', 'Pizza']

    # Determinar clase predicha
    predicted_class = class_labels[int(y_pred)]

    print(f'El modelo identificó: {predicted_class}')

# Ejecutar función principal
AI()
