from flask import Flask, render_template, request, jsonify, send_file
from srcnn import SRCNN
from PIL import Image
from flask_cors import CORS, cross_origin
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove
import base64
import re
import io
app = Flask(__name__, static_folder='./build', static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
srcnn = SRCNN()

@app.route('/', methods=['GET', 'POST'])
def load():
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    
    f = request.files['image']
    
    print(f)
    prediction, score = srcnn.predict(f)
    # img = Image.fromarray(prediction.astype('uint8'))
    # file_obj = io.BytesIO()

    # img.save(file_obj, 'PNG')
    # file_obj.seek(0)

    # tempFileObj = NamedTemporaryFile(mode='w+b', suffix='png')
    # with open('/Users/khabiirkhodabaccus/Desktop/tutorial/SRCNN-webapp/static/tmp.png', 'rb') as tmp:
    #      encoded_string = base64.b64encode(tmp.read())
         #copyfileobj(tmp, tempFileObj)

    encoded_string = base64.b64encode(prediction)
    
    # remove("/Users/khabiirkhodabaccus/Desktop/tutorial/SRCNN-webapp/static/tmp.png")
    # tempFileObj.seek(0,0)

    # response = send_file(tempFileObj, as_attachment=True, attachment_filename='predicted.png')
    result = {'data' : encoded_string.decode('utf-8'), 'score' : score}
    return jsonify(result)


if __name__ == '__main__':
    app = Flask(__name__, static_folder='./build', static_url_path='/')
    app.run(host='localhost', port=3000)