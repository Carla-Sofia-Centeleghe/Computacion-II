import logging
import numpy as np
import redis # type: ignore
from celery import Celery
from tensorflow import keras # type: ignore
from PIL import Image

def make_celery():
    backend = 'redis://localhost:6379/0'  # Redis como backend
    broker = 'redis://localhost:6379/0'   # Redis como broker
    return Celery('food_detector', backend=backend, broker=broker)

celery = make_celery()

# Configurar logger para Celery
celery_log = logging.getLogger('celery_task')
celery_log.setLevel(logging.INFO)

# Configurar Redis como cliente
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@celery.task(name="app.classify_image")
def classify_image_task(filepath):
    celery_log.info(f"Clasificando imagen en {filepath}")
    
    try:
        model = keras.models.load_model('simple_cnn_model.keras')
        img = Image.open(filepath)
        img = img.resize((150, 150))
        img_array = np.expand_dims(np.array(img), axis=0)
        predictions = model.predict(img_array)
        result = 'Pizza' if predictions[0] > 0.5 else 'Carne'
        celery_log.info(f"Resultado de la clasificación: {result}")
        return result
    except Exception as e:
        celery_log.error(f"Error procesando la imagen: {e}")
        return f"Error processing image: {e}"
    
@celery.task(name="log_processor.log_task")
def log_to_redis(log_entry):
    # Almacena el log en Redis
    redis_client.rpush('log_channel', log_entry)  # Agrega el log a una lista llamada log_channel

# Crear logger para la aplicación
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)

# Puedes añadir un StreamHandler para imprimir en consola si deseas
console_handler = logging.StreamHandler()
app_logger.addHandler(console_handler)

def log(message):
    # Envía el log a Celery
    log_to_redis.delay(message)