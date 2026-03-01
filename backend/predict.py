import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.models.load_model("../models/densenet121_model.h5")

classes = ["normal","benign","malignant"]


def predict_image(path):

    img = cv2.imread(path)

    img = cv2.resize(img,(224,224))

    img = img/255.0

    img = np.reshape(img,(1,224,224,3))

    prediction = model.predict(img)

    return classes[np.argmax(prediction)]