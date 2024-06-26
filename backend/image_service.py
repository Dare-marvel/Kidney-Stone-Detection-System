import io

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image
import base64

loaded_model = tf.keras.models.load_model("backend/bin/model.h5")
label_to_class_name = {0: 'Cyst', 1: 'Normal', 2: 'Stone', 3: 'Tumor'}


def predict_and_plot(img):
    # Resize the image and predict the label
    resize = tf.image.resize(img, (150, 150))
    yhat = loaded_model.predict(np.expand_dims(resize / 255, 0))
    max_index = np.argmax(yhat)
    predicted_label = label_to_class_name[max_index]

    # Plot the image
    plt.imshow(img)
    plt.title(predicted_label)
    plt.axis('off')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert BytesIO to PIL Image
    image = Image.open(buf)

    # Convert image to RGB mode
    image = image.convert('RGB')

    # Convert PIL Image to byte array
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')

    # Encode byte array to base64 string
    encoded_image = base64.b64encode(byte_arr.getvalue()).decode('utf-8')

    return predicted_label, encoded_image
