import os, sys
import base64
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask import request
from flask import jsonify
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-001')

app = Flask(__name__)

def get_qa_response(image_path):
    sample_file = genai.upload_file(path=image_path, display_name="question")
    response = model.generate_content(
        [f"Solve the given question and answer in step wise", sample_file]
    )
    genai.delete_file(sample_file.name)
    return response.text

@app.route("/test", methods=['GET'])
def test():
    return jsonify({'success' : 'true'})

@app.route("/", methods=['POST'])
def qa():
    b64_img = request.form['image']
    img_path = "static/images/ques_img.png"
    with open(img_path, "wb") as img_f:
        img_f.write(base64.b64decode(b64_img))
    ans = get_qa_response(image_path=img_path)
    return jsonify({'answer' : ans})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)