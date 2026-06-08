import tensorflow as tf
from tensorflow.keras import layers, models
from config import Config

def build_efficientnet_ensemble():
    """Builds and returns the custom EfficientNet model graph as specified in experiment."""
    base_model = tf.keras.applications.EfficientNetB0(
        weights='imagenet', 
        include_top=False, 
        input_shape=(Config.IMG_HEIGHT, Config.IMG_WIDTH, Config.CHANNELS)
    )
    base_model.trainable = False  # Freeze backbone for initial stages
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(name="global_average_pooling2d"),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(Config.NUM_CLASSES, activation='softmax', name="dense_prediction")
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
