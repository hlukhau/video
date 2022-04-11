from flask import Flask, render_template, request, session, redirect
import cv2
import os
import glob

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():
    scene = ""
    video = ""
    if (os.path.exists('static/projects/demo/scene/scene.jpg')):
        scene = '/static/projects/demo/scene/scene.jpg'
        print(scene)

        if (os.path.exists('static/projects/demo/video/small.jpg')):
            video = '/static/projects/demo/video/small.jpg'
            print(video)
    else:
        print('no scene')

    if session.get('project') == None:
        session['project'] = 'Undefined'

    print("Session project: " + session.get('project'))
    return render_template('main.html', project="Example project", scene=scene, video=video)
#    return "Index Page - goto <a href='/hello?coords=[[10,20],[30,13]]&param=[1200,600]'>hello</a><br>or go to drag and drop page <a href='static/drag-drop.html'>PAGE</a><br>go to <a href='static/main.html'>Bootstrap</a> page"


@app.route('/content', methods=['POST', 'GET'])
def content():
    if request.method == "POST":
        data = request.get_json()
        session['project'] = data['project']

    scene = ""
    video = ""
    if (os.path.exists('static/projects/demo/scene/scene.jpg')):
        scene = '/static/projects/demo/scene/scene.jpg'
        print(scene)

    if (os.path.exists('static/projects/demo/video/small.jpg')):
        video = '/static/projects/demo/video/small.jpg'
        print(video)

    print("Session project: " + session.get('project'))

    return render_template('content.html', project="Example project", scene=scene, video=video)


@app.route('/hello')
def hello():
    coords = request.args.get('coords')
    param = request.args.get('param')
    return "Hello World - goto <a href='/upload'>upload</a> Coords: " + coords + " Param: " + param


@app.route('/upload')
def upload_html():
    path = request.args.get('path')
    return render_template('upload.html', path=path)

@app.route('/send', methods=['GET', 'POST'])
def send_file():
    path = request.args.get('path')
    print("send: " + path)

    if request.method == 'POST':
        f = request.files['file']
        print("path: " + path + f.filename)

        if path.find("scene") != -1:
            print("save")
            f.save("static/projects/demo/scene/scene.jpg")

        if path.find("video") != -1:
            f.save("static/projects/demo/video/video.mp4")
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
                cv2.imwrite("static/projects/demo/video/small.jpg", resized)  # save frame as JPEG file

        return redirect('/')

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
        return redirect('/')


@app.route('/drag-drop')
def drop_down_upload():
    path = request.args.get('path')
    message = request.args.get('message')
    return render_template('drag-drop.html', path=path, message=message)


@app.route('/remove')
def remove():
    path = request.args.get('path')

    if path.find("scene") != -1:
        os.remove("static/projects/demo/scene/scene.jpg")

    if path.find("video") != -1:
        os.remove("static/projects/demo/video/small.jpg")
        os.remove("static/projects/demo/video/video.mp4")

    return redirect('/')


@app.route('/exit')
def exit():
    session.pop('project', None)
    return redirect('/')


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'files'
    app.run(host='0.0.0.0', port=5555)



