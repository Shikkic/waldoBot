import os
import cv2
import numpy as np
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/dcadden/dev/python/imgs'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        print("request is post!")
        file = request.files['file']
        if file and allowed_file(file.filename):
            print("request has both a file, and is secure")
            filename = secure_filename(file.filename)
            print("file is secured")
            print("saving file to "+os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print("File has been saved")

    print("Made it past the request with file="+filename)
    
    img = cv2.imread('imgs/'+filename);

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    ORANGE_MIN = np.array([0, 160, 120],np.uint8)
    ORANGE_MAX = np.array([10, 255, 255],np.uint8) 

    mask = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)

    res = cv2.bitwise_and(hsv_img, hsv_img, mask= mask)
    cv2.imwrite(filename, res)
    return "Hello World!"

if __name__ == "__main__":
    app.run()
