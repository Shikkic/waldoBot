import os
import cv2
import numpy as np
from scipy.ndimage.morphology import binary_dilation
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/Users/charleslai/Documents/Programming/other-projects/waldoBot/server/imgs'
UPLOAD_FOLDER = '/Users/dcadden/dev/hackny/python/waldoBot/server/imgs'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['POST'])
def hello():
    try:
        if request.method == "POST":
            file = request.files['file']
            if file and allowed_file(file.filename):
                print("request has both a file, and is secure")
                filename = secure_filename(file.filename)
                print("file is secured")
                print("saving file to "+os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                print("File has been saved")

                print("Made it past the request with file="+filename)

                # Read in file
                waldo = cv2.imread('imgs/'+filename)

                # Resize 
                waldo = cv2.resize(waldo, None, fx=.4, fy=.4, interpolation = cv2.INTER_AREA)

                # Separate color channels
                waldo_float = waldo.astype(float)

                # Gaussian Blur to reduce noise
                waldo_float = cv2.GaussianBlur(waldo_float, (3,3), 0)
                
                b,g,r = cv2.split(waldo_float)
                w = waldo_float.mean(2)

                # Create a convolution kernel representing a red and white shirt
                pattern = np.ones((24,16), float)
                for i in xrange(2):
                    pattern[i::4] = -1

                # Convolve with red less white to find Waldo's shirt
                v = cv2.filter2D(r-w, -1, pattern)

                # Create a mask to bring out probable locations of Waldo
                mask = (v >= v.max()-(v.max()/3))
                mask = binary_dilation(mask, np.ones((48,24)))
                waldo -= .8*waldo * ~mask[:,:,None]

                # Overwrite file with resulting file
                cv2.imwrite('result/'+filename, waldo)

                # Return url handle of new image
                return "result/"+filename
            else:
                return "Bad filename"
        else:
            return "Must use sick bars."
    except Exception, e:
        print e
        return e

@app.route('/result/<path:path>')
def send_js(path):
    return send_from_directory('result', path)
    
if __name__ == "__main__":
    app.run()
