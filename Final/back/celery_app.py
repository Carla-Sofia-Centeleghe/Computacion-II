import logging
import numpy as np
import redis # type: ignore
from celery import Celery
from tensorflow import keras # type: ignore
from PIL import Image

# Configuramos el broker y el backend de Celery, usando Redis
app = Celery('image_classification',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

app.conf.update(
    result_expires=3600,            # Expira el resultado de la tarea después de 1 hora
    task_serializer='json',         # Serializa las tareas en formato JSON
    accept_content=['json'],        # Acepta contenido en formato JSON
    result_serializer='json',       # Serializa los resultados en formato JSON
    worker_prefetch_multiplier=1,   # Prefetching de tareas para cada worker
    task_time_limit=300,            # Límite de tiempo de ejecución de la tarea en segundos
    enable_utc=True,                # Habilita el uso de UTC para la planificación de tareas
    timezone='UTC'
)

# Configuramos el logger de Celery
celery_log = logging.getLogger('celery_logger')
celery_log.setLevel(logging.INFO)
redis_cli = redis.StrictRedis(host='localhost', port=6379, db=0)

# Configuramos la tarea de celery
@app.task(name='classify_image_task')
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
    

@app.task(name="log_processor.log_task")
def log_to_redis(log_entry):
    redis_cli.rpush('log_channel', log_entry)  # Agrega el log a una lista llamada log_channel

# Crearmos logger para la aplicación
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)

# Configuramos un handler de archivo para el logger de la aplicación
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Configuramos un formatter y agregarlo al handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Agregarmos el handler al logger de la aplicación
app_logger.addHandler(file_handler)

def log(message):
    # Envíamos el log a Celery
    log_to_redis.delay(message)