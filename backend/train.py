import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers, models
from utils.preprocess import load_data

train_path = "../dataset/train"
test_path = "../dataset/test"

train_dataset, test_dataset = load_data(train_path, test_path)

base_model = DenseNet121(

    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)

)

base_model.trainable = False


x = base_model.output

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dense(256,activation='relu')(x)

x = layers.Dropout(0.5)(x)

output = layers.Dense(3,activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)


model.compile(

    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']

)


history = model.fit(

    train_dataset,
    validation_data=test_dataset,
    epochs=20

)

model.save("../models/densenet121_model.h5")

print("Training Complete")