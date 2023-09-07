from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"

@app.route("/python")
def hello_world():
    return "<p>Hello, Python!</p>"

@app.route('/generate_video', methods=['POST'])
def generate_video():
    # NOTE: currently only sending image as a test, eventually video will be sent
    return send_file('python_module/generated/final_image.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
