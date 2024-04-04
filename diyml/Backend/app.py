from flask import Flask
from Auth_api import auth_blueprint
from inference_api import infer_blueprint

app = Flask(__name__)
app.register_blueprint(auth_blueprint)
app.register_blueprint(infer_blueprint)

if __name__ == "__main__":
    app.run(debug=True)