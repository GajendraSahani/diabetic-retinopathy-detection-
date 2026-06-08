import cv2
import numpy as np
import tensorflow as tf
from config import Config

class DataPipeline:
    @staticmethod
    def read_image(path):
        # Convert path tensor to string safely
        if isinstance(path, tf.Tensor):
            path = path.numpy().decode('utf-8')
        img = cv2.imread(path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def crop_black(img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray > 10
        return img[np.ix_(mask.any(1), mask.any(0))]

    @classmethod
    def preprocess_image_pipeline(cls, path):
        # Wrapper logic matching notebook implementation
        img = cls.read_image(path)
        img = cls.crop_black(img)
        img = cv2.resize(img, Config.IMG_SIZE)
        img = img.astype(np.float32) / 255.0
        return img

    @classmethod
    def tf_parse_function(cls, filename, label):
        [image,] = tf.py_function(lambda p: [cls.preprocess_image_pipeline(p)], [filename], [tf.float32])
        image.set_shape((Config.IMG_HEIGHT, Config.IMG_WIDTH, Config.CHANNELS))
        label = tf.one_hot(label, Config.NUM_CLASSES)
        return image, label

    @classmethod
    def build_dataset(cls, filenames, labels, is_training=True):
        dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
        dataset = dataset.shuffle(buffer_size=len(filenames)) if is_training else dataset
        dataset = dataset.map(cls.tf_parse_function, num_parallel_calls=Config.AUTOTUNE)
        return dataset.batch(Config.BATCH_SIZE).prefetch(Config.AUTOTUNE)
