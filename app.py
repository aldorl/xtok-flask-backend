from flask import Flask, send_file
from flask_cors import CORS
import subprocess

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
    # NOTE: following line only sending image as a test, eventually video will be sent
    # return send_file('python_module/generated/final_image.png', mimetype='image/png')
    try:
        print("Trying python subprocess", flush=True)
        subprocess.call("python3 python_module/main.py", shell=True)
    except Exception as e:
        print("Exception caught", flush=True)
        print(str(e), flush=True)

    try:
        print("About to send file...", flush=True)
        return send_file('python_module/generated/output_video.mp4', mimetype='video/mp4')
    except Exception as e:
        print("Exception caught", flush=True)
        print(str(e), flush=True)
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
