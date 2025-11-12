# Модуль нейронной сети для классификации изображений
# Использует предобученную модель ResNet50V2

import os
# Используем бесплатный план и экономим мощности при работе с нейросетью
# Уменьшаем логи TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import random
import keras
from keras.layers import Input
from keras.models import Model
from keras.applications.resnet_v2 import ResNet50V2, preprocess_input, decode_predictions
import numpy as np
from PIL import Image

# Параметры изображения для нейросети
height = 224
width = 224
nh = 224
nw = 224
ncol = 3

# Глобальная переменная для модели
_resnet_model = None

def get_resnet_model():
    # Загружает и возвращает модель ResNet (синглтон)
    global _resnet_model
    if _resnet_model is None:
        print("Initializing ResNet model...")
        visible2 = Input(shape=(nh, nw, ncol), name='imginp')
        _resnet_model = ResNet50V2(include_top=True,weights='imagenet',
            input_tensor=visible2,input_shape=None,pooling=None,classes=1000)

        # "Прогрев" модели
        dummy_input = np.random.random((1, height, width, 3))
        _ = _resnet_model.predict(dummy_input, verbose=0)
        print("ResNet model ready!")
    return _resnet_model

def read_image_files(files_max_count, dir_name):
    # Читает изображения из директории
    files = [item.name for item in os.scandir(dir_name) if item.is_file() and item.name.lower().endswith(('.png', '.jpg', '.jpeg'))]
    files_count = min(files_max_count, len(files))
    image_box = []

    for file_i in range(files_count):
        try:
            img_path = os.path.join(dir_name, files[file_i])
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_box.append(img)
        except Exception as e:
            print(f"Ошибка загрузки {files[file_i]}: {e}")
            continue

    return len(image_box), image_box

def getresult(image_box):
    # Классифицирует изображения с помощью нейросети
    if not image_box:
        return [[('no_image', 'no_image', 0.0)]]

    model = get_resnet_model()
    files_count = len(image_box)
    images_resized = np.zeros((files_count, height, width, 3))

    # Предобработка изображений
    for i in range(files_count):
        try:
            img_resized = image_box[i].resize((height, width))
            img_array = np.array(img_resized, dtype=np.float32)

            if len(img_array.shape) == 2:
                img_array = np.stack([img_array] * 3, axis=-1)
            elif img_array.shape[2] == 4:
                img_array = img_array[:, :, :3]

            images_resized[i] = img_array
        except Exception as e:
            print(f"Ошибка обработки изображения {i}: {e}")
            images_resized[i] = np.zeros((height, width, 3))
    # Нормализация и предобработка для ResNet
    images_resized = images_resized / 255.0
    images_resized = preprocess_input(images_resized)

    try:
        # Классификация
        out_net = model.predict(images_resized, verbose=0, batch_size=1)
        decode = decode_predictions(out_net, top=1)
        return decode
    except Exception as e:
        print(f"Ошибка классификации: {e}")
        return [[('prediction_error', 'prediction_error', 0.0)]]

# Предзагрузка модели при импорте модуля
print("Preloading neural network...")
get_resnet_model()
