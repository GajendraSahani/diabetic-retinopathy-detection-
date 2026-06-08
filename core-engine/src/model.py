import tensorflow as tf
from tensorflow.keras import layers, models
from config import Config

def build_efficientnet_backbone():
    base_model = tf.keras.applications.EfficientNetB0(
        weights='imagenet', 
        include_top=False, 
        input_shape=(Config.IMG_HEIGHT, Config.IMG_WIDTH, Config.CHANNELS)
    )
    base_model.trainable = False  # Freeze initial layer groups
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(name="global_average_pooling2d"),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(Config.NUM_CLASSES, activation='softmax', name="dense_prediction")
    ], name="Production_EfficientNet_Classifier")
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def build_mobilenet_backbone():
    base_model = tf.keras.applications.MobileNetV3Large(
        weights='imagenet',
        include_top=False,
        input_shape=(Config.IMG_HEIGHT, Config.IMG_WIDTH, Config.CHANNELS)
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(name="global_average_pooling2d_mobilenet"),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(Config.NUM_CLASSES, activation='softmax', name="prediction_layer")
    ], name="Production_MobileNet_Classifier")
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
