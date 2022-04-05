from flask import Flask, render_template, request
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return "Index Page - goto <a href='/hello?coords=[[10,20],[30,13]]&param=[1200,600]'>hello</a><br>or go to drag and drop page <a href='static/drag-drop.html'>PAGE</a><br>go to <a href='static/main.html'>Bootstrap</a> page"


@app.route('/hello')
def hello():
    coords = request.args.get('coords')
    param = request.args.get('param')
    return "Hello World - goto <a href='/upload'>upload</a> Coords: " + coords + " Param: " + param


@app.route('/upload')
def upload_html():
    return render_template('upload.html')

@app.route('/send', methods=['GET', 'POST'])
def send_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('files/' + f.filename)
        return "file uploaded successfully"


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('files/' + f.filename)
        sub = cv2.VideoCapture('files/' + f.filename)
        sub.set(cv2.CAP_PROP_POS_MSEC, 2000)  # just cue to 20 sec. position
        success, image = sub.read()
        if success:
            print('success')
            h, w, _ = image.shape
            width = int(w)
            height = int(h)
            height = int(128 * height / width)
            width = 128
            print(w, h)
            print(width, height)
            resized = cv2.resize(image, (width, height))
            cv2.imwrite('static/' + f.filename + ".jpg", image)  # save frame as JPEG file
            cv2.imwrite('static/' + f.filename + "s.jpg", resized)  # save frame as JPEG file
        return "file uploaded successfully<br /><img src='" + 'static/' + f.filename + "s.jpg" + "'><br><img src='" + 'static/' + f.filename + ".jpg" + "'>"


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'files'
    app.run(host='0.0.0.0', port=5555)
