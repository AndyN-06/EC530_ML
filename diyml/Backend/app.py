from flask import Flask
from flask_cors import CORS
from Auth_api import auth_blueprint
from inference_api import infer_blueprint
from data_upload_api import upload_blueprint

app = Flask(__name__)
app.register_blueprint(auth_blueprint)
app.register_blueprint(infer_blueprint)
app.register_blueprint(upload_blueprint)

CORS(app)

if __name__ == "__main__":
    app.run(debug=True)