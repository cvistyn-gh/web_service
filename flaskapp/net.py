import random
import keras
from keras.layers import Input
from keras.models import Model
from keras.applications.resnet_v2 import ResNet50V2, preprocess_input, decode_predictions
# from keras.applications.resnet50 import preprocess_input, decode_predictions
import os
# from PIL import Image
import PIL.Image as Image
import numpy as np
# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.7
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)

height = 224
width = 224
nh=224
nw=224
ncol=3

visible2 = Input(shape=(nh,nw,ncol),name = 'imginp')
resnet = ResNet50V2(include_top=True,
                   weights='imagenet',
                   input_tensor=visible2,
                   input_shape=None,
                   pooling=None,
                   classes=1000)

def read_image_files(files_max_count, dir_name):
    files = [item.name for item in os.scandir(dir_name) if item.is_file() and item.name.lower().endswith(('.png', '.jpg', '.jpeg'))]
    files_count = min(files_max_count, len(files))
    image_box = []

    for file_i in range(files_count):
        try:
            img_path = os.path.join(dir_name, files[file_i])
            img = Image.open(img_path)
            # Конвертируем в RGB если нужно
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_box.append(img)
        except Exception as e:
            print(f"Ошибка загрузки {files[file_i]}: {e}")
            continue

    return len(image_box), image_box

def getresult(image_box):
    if not image_box:
        return [[('no_image', 'no_image', 0.0)]]

    files_count = len(image_box)

    # Исправление: создаем правильный массив
    images_resized = np.zeros((files_count, height, width, 3))

    for i in range(files_count):
        try:
            img_resized = image_box[i].resize((height, width))
            img_array = np.array(img_resized, dtype=np.float32)

            # Если изображение grayscale, преобразуем в RGB
            if len(img_array.shape) == 2:
                img_array = np.stack([img_array] * 3, axis=-1)
            elif img_array.shape[2] == 4:  # RGBA -> RGB
                img_array = img_array[:, :, :3]

            images_resized[i] = img_array

        except Exception as e:
            print(f"Ошибка обработки изображения {i}: {e}")
            # Заполняем черным изображением в случае ошибки
            images_resized[i] = np.zeros((height, width, 3))

    # Нормализуем и предобрабатываем
    images_resized = images_resized / 255.0
    images_resized = preprocess_input(images_resized)

    try:
        out_net = resnet.predict(images_resized)
        decode = decode_predictions(out_net, top=1)
        return decode
    except Exception as e:
        print(f"Ошибка классификации: {e}")
        return [[('prediction_error', 'prediction_error', 0.0)]]
