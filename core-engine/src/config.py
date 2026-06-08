import os
import tensorflow as tf

class Config:
    SEED = 42
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    IMG_SIZE = (IMG_HEIGHT, IMG_WIDTH)
    CHANNELS = 3
    NUM_CLASSES = 5
    BATCH_SIZE = 32
    EPOCHS = 30
    LEARNING_RATE = 1e-4
    AUTOTUNE = tf.data.AUTOTUNE
    
    DATASET_DIR = "./aptos_dataset"
    TRAIN_CSV = os.path.join(DATASET_DIR, "train.csv")
    TRAIN_IMAGE_DIR = os.path.join(DATASET_DIR, "train_images")
