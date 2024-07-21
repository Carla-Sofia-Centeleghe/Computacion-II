import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Función principal
def AI():
    # Configuración de los directorios de datos
    train_dir = '/home/carla/Documentos/GitHub/Computacion-II/Final/back/train_dir'
    validation_dir = '/home/carla/Documentos/GitHub/Computacion-II/Final/back/validation_dir'

    # Crear generadores de imágenes para entrenamiento y validación
    train_datagen = ImageDataGenerator(rescale=1./255)
    validation_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(150, 150),  # Tamaño de las imágenes de entrada
            batch_size=32,
            class_mode='binary')

    validation_generator = validation_datagen.flow_from_directory(
            validation_dir,
            target_size=(150, 150),
            batch_size=32,
            class_mode='binary')

    # Construir la red neuronal / Denir el modelo
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(1, activation='sigmoid')  # Capa de salida binaria
    ])

    # Compilar el modelo
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])

    # Entrenar el modelo
    history = model.fit(
        train_generator,
        steps_per_epoch=100,  # Número de lotes por época
        epochs=15,
        validation_data=validation_generator,
        validation_steps=50)

    # Guardar el modelo
    model.save('simple_cnn_model.keras')

    # Usar el modelo para clasificar nuevas imágenes
    #new_image_path = '/home/carla/Documentos/GitHub/Computacion-II/Final/back/train_dir/pizza/22489.jpg'
    #img_array = tf.keras.preprocessing.image.load_img(new_image_path, target_size=(150, 150))
    #img_array = tf.keras.preprocessing.image.img_to_array(img_array)
    #img_array = tf.expand_dims(img_array, 0)

    #predictions = model.predict(img_array)
    #print(predictions)

    # Interpretar la predicción
    #predicted_class = 'Pizza' if predictions > 0.5 else 'Carne'
    #print(f'El modelo identificó: {predicted_class}')

# Ejecutar función principal
AI()