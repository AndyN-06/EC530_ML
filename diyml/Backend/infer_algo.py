import sqlite3
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import os

def predict(project_id, image_path):
    DB = 'ml.db'
    DATABASE = os.path.join(os.path.dirname(__file__), DB)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT model_id, model FROM Models WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No model found for the given project ID")
        model_id, blob = row

        # Load model from blob
        model_path = os.path.join(os.path.dirname(__file__), f'model_{model_id}.h5')
        with open(model_path, 'wb') as file:
            file.write(blob)
        model = load_model(model_path)

    img = image.load_img(image_path, (128,128))
    img_array = img.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array).flatten().tolist()

    cursor.execute("INSERT INTO Inferences (model_id, image_path, result) VALUES (?, ?, ?)", (model_id, image_path, prediction[0]))
    cursor.commit()
    conn.close()
