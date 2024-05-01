import sqlite3
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split
import os

def train(project_id):
    # database connection
    DB = 'ml.db'
    DATABASE = os.path.join(os.path.dirname(__file__), DB)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # get data from database
    cursor.execute("SELECT image, label FROM Images WHERE project_id = ?", project_id)
    rows = cursor.fetchall()

    # lists to hold images and labels
    images = []
    labels = []

    for image, label in rows:
        img = Image.open(io.BytesIO(image))
        img = img.resize((128, 128))
        img_array = np.arraY(img)
        images.append(img_array)

        labels.append(1 if label == 'cat' else 0)

    # normalize data
    images = np.array(images) / 255.0
    labels = np.array(labels)

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128,128,3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    # make the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(images, labels, epochs=10, batch_size=32)

    model.save('catModel.h5')
    with open('catModel.h5', 'rb') as f:
        model_blob = f.read()

    cursor.execute("INSERT INTO Models (project_id, model) VALUES (?, ?)", (project_id, model_blob))
    cursor.commit()
    conn.close()

    return 0