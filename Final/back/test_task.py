from app import classify_image
from celery import Celery

app = Celery('app.celary', broker='redis://localhost:6379/0')

# Llama a la tarea
result = classify_image.delay('/home/carla/Documentos/GitHub/Computacion-II/Final/back/train_dir/pizza/40449.jpg')

# Imprime el resultado
print(f'Task ID: {result.id}')
print(f'Status: {result.status}')

# Espera el resultado
predicted_class = result.get(timeout=45)  # Ajusta el timeout según sea necesario

# Imprime el resultado de la clasificación
print(f'El modelo identificó: {predicted_class}')
