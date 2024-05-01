import sqlite3
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import os

def predict(project_id, image_path):
    DB = 'ml.db'
    DATABASE = os.path.join(os.path.dirname(__file__), DB)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT model FROM Models WHERE project_id = ?", (project_id))
    model_id = cursor.fetchone()[0]
    blob = cursor.fetchone()[2]
    path = 'model.h5'
    with open(path, 'wb') as file:
        file.write(blob)
    model = load_model(path)

    img = image.load_img(image_path, (128,128))
    img_array = img.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array)

    cursor.execute("INSERT INTO Inferences (model_id, image_path, result) VALUES (?, ?, ?)", (model_id, image_path, prediction))
    cursor.commit()
    conn.close()
