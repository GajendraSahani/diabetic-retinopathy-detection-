import cv2
import numpy as np
import tensorflow as tf
from config import Config

class DataPipeline:
    @staticmethod
    def read_image(path):
        if isinstance(path, tf.Tensor):
            path = path.numpy().decode('utf-8')
        img = cv2.imread(path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def crop_black(img):
        """Crops out black space padding borders as defined in Stage 2 of the notebook."""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray > 10
        if not np.any(mask):
            return img
        return img[np.ix_(mask.any(1), mask.any(0))]

    @staticmethod
    def apply_clahe(img):
        """Applies Contrast Limited Adaptive Histogram Equalization mapping to the L channel."""
        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    @classmethod
    def preprocess_image_pipeline(cls, path):
        """Executes the exact image engineering chain built during data preparation stages."""
        img = cls.read_image(path)
        img = cls.crop_black(img)
        img = cls.apply_clahe(img)
        
        # Gaussian Denoise, resizing, and fractional mapping normalization
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.resize(img, Config.IMG_SIZE)
        img = img.astype(np.float32) / 255.0
        return img

    @classmethod
    def tf_parse_function(cls, filename, label):
        """Wrapper method converting input stream signatures into safe TensorFlow tensors."""
        [image,] = tf.py_function(lambda p: [cls.preprocess_image_pipeline(p)], [filename], [tf.float32])
        image.set_shape((Config.IMG_HEIGHT, Config.IMG_WIDTH, Config.CHANNELS))
        label = tf.one_hot(label, Config.NUM_CLASSES)
        return image, label

    @classmethod
    def build_dataset_pipeline(cls, filenames, labels, is_training=True):
        """Constructs an unbuffered input-bound pipeline for dataset operations."""
        dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
        if is_training:
            dataset = dataset.shuffle(buffer_size=len(filenames), seed=Config.SEED)
        dataset = dataset.map(cls.tf_parse_function, num_parallel_calls=Config.AUTOTUNE)
        return dataset.batch(Config.BATCH_SIZE).prefetch(Config.AUTOTUNE)
