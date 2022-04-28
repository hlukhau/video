from flask import Flask, render_template, request, session, redirect
import cv2
import os
import json
import glob
import time
import cv2
import numpy as np
from multiprocessing import Process, Value

from pydub import AudioSegment
from pydub.playback import play
# from ffpyplayer.player import MediaPlayer

#from processunix import video_player
import translation as tr

app = Flask(__name__)
app.secret_key = "super secret key"
run = Value('d', 1.0)


@app.route('/')
def index():
    scene = ""
    video = ""

    if session.get('project') == None:
        session['project'] = 'demo'

    project = session.get('project')

    if (os.path.exists('static/projects/' + project + '/scene/scene.jpg')):
        scene = '/static/projects/' + project + '/scene/scene.jpg'

        if (os.path.exists('static/projects/' + project + '/video/small.jpg')):
            video = '/static/projects/' + project + '/video/small.jpg'


    with open('files/projects.json') as json_file:
        projects = json.load(json_file)

    return render_template('main.html', project=project, scene=scene, video=video, projects=projects)
#    return "Index Page - goto <a href='/hello?coords=[[10,20],[30,13]]&param=[1200,600]'>hello</a><br>or go to drag and drop page <a href='static/drag-drop.html'>PAGE</a><br>go to <a href='static/main.html'>Bootstrap</a> page"



@app.route('/projects', methods=['GET'])
def projects():
    with open('files/projects.json') as json_file:
        data = json.load(json_file)


@app.route('/content', methods=['POST', 'GET'])
def content():
    project = session['project']

    if request.method == "POST":
        data = request.get_json()

        if "project" in data:
            tmp = data.get('project')

            if tmp != 'Undefined':
                session['project'] = data['project']
                project = data['project']
                if (os.path.exists('static/projects/' + project) != True):
                    os.mkdir('static/projects/' + project)
                    os.mkdir('static/projects/' + project + '/scene')
                    os.mkdir('static/projects/' + project + '/video')

    scene = ""
    video = ""
    project = session['project']

    if (os.path.exists('static/projects/' + project + '/scene/scene.jpg')):
        scene = '/static/projects/' + project + '/scene/scene.jpg'

    if (os.path.exists('static/projects/' + project + '/video/small.jpg')):
        video = '/static/projects/' + project + '/video/small.jpg'

    return render_template('content.html', project=session['project'], scene=scene, video=video)


@app.route('/hello')
def hello():
    coords = request.args.get('coords')
    param = request.args.get('param')
    return "Hello World - goto <a href='/upload'>upload</a> Coords: " + coords + " Param: " + param


@app.route('/upload')
def upload_html():
    path = request.args.get('path')
    return render_template('upload.html', path=path)


@app.route('/add')
def add_project():
    name = request.args.get('name')
    with open('files/projects.json') as json_file:
        projects = json.load(json_file)
        element = {"name":name}
        exists = element in projects

        if not exists:
            projects.append(element)
            print(projects)

            with open('files/projects.json', 'w') as outfile:
                json.dump(projects, outfile)
                session['project'] = name

                if (os.path.exists('static/projects/' + name) != True):
                    os.mkdir('static/projects/' + name)
                    os.mkdir('static/projects/' + name + '/scene')
                    os.mkdir('static/projects/' + name + '/video')

    return redirect('/')

@app.route('/points', methods=['POST'])
def points():
    project = session['project']
    points = request.get_json()

    with open('static/projects/' + project + '/displays.json', 'w') as outfile:
        json.dump(points, outfile)
    return "Ok"



@app.route('/send', methods=['GET', 'POST'])
def send_file():
    project = session['project']
    path = request.args.get('path')

    if request.method == 'POST':
        f = request.files['file']

        if path.find("scene") != -1:
            f.save("static/projects/" + project + "/scene/scene.jpg")

        if path.find("video") != -1:
            f.save("static/projects/" + project + "/video/video.mp4")
            sub = cv2.VideoCapture('files/' + f.filename)
            sub.set(cv2.CAP_PROP_POS_MSEC, 2000)  # just cue to 20 sec. position
            success, image = sub.read()

            if success:
                h, w, _ = image.shape
                width = int(w)
                height = int(h)
                height = int(128 * height / width)
                width = 128
                resized = cv2.resize(image, (width, height))
                cv2.imwrite("static/projects/" + project + "/video/original.jpg", image)  # save frame as JPEG file
                cv2.imwrite("static/projects/" + project + "/video/small.jpg", resized)  # save frame as JPEG file

        time.sleep(1)
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
            h, w, _ = image.shape
            width = int(w)
            height = int(h)
            height = int(128 * height / width)
            width = 128
            resized = cv2.resize(image, (width, height))
            cv2.imwrite('static/' + f.filename + ".jpg", image)  # save frame as JPEG file
            cv2.imwrite('static/' + f.filename + "s.jpg", resized)  # save frame as JPEG file
        return redirect('/')


@app.route('/drag-drop')
def drop_down_upload():
    path = request.args.get('path')
    message = request.args.get('message')
    return render_template('drag-drop.html', path=path, message=message)


@app.route('/delete')
def delete():
    project = session.get('project')
    element = {"name": project}

    if (os.path.exists('static/projects/' + project + '/scene/scene.jpg')):
        os.remove("static/projects/" + project + "/scene/scene.jpg")

    if (os.path.exists('static/projects/' + project + '/video/small.jpg')):
        os.remove("static/projects/" + project + "/video/small.jpg")
    if (os.path.exists('static/projects/' + project + '/video/original.jpg')):
        os.remove("static/projects/" + project + "/video/original.jpg")
    if (os.path.exists('static/projects/' + project + '/video/video.mp4')):
        os.remove("static/projects/" + project + "/video/video.mp4")

    os.rmdir("static/projects/" + project + "/scene")
    os.rmdir("static/projects/" + project + "/video")
    os.rmdir("static/projects/" + project)

    with open('files/projects.json') as json_file:
        projects = json.load(json_file)

        projects.remove(element)
        with open('files/projects.json', 'w') as outfile:
            json.dump(projects, outfile)
            session['project'] = 'demo'

    session['project'] = 'demo'

    return redirect('/')



@app.route('/edit')
def edit():
    project = session.get('project')
    path = request.args.get('path')
    print("edit: " + path)
    points = []

    if (os.path.exists('static/projects/' + project + '/displays.json')):
        print('static/projects/' + project + '/displays.json')
        with open('static/projects/' + project + '/displays.json') as points_file:
            points = json.load(points_file)

    print(points)
    return render_template('canvas-viewer.html', path=path, project=project, points=points)


@app.route('/remove')
def remove():
    project = session.get('project')
    path = request.args.get('path')

    if path.find("scene") != -1:
        if (os.path.exists('static/projects/' + project + '/scene/scene.jpg')):
            os.remove("static/projects/" + project + "/scene/scene.jpg")

    if path.find("video") != -1:
        if (os.path.exists('static/projects/' + project + '/video/small.jpg')):
            os.remove("static/projects/" + project + "/video/small.jpg")
        if (os.path.exists('static/projects/' + project + '/video/original.jpg')):
            os.remove("static/projects/" + project + "/video/original.jpg")
        if (os.path.exists('static/projects/' + project + '/video/video.mp4')):
            os.remove("static/projects/" + project + "/video/video.mp4")

    return redirect('/')


@app.route('/exit')
def exit():
    session.pop('project', None)
    return redirect('/')


@app.route('/start-video')
def start_video():
    project = session.get('project')
    print('start video ' + project)

    if (os.path.exists('static/projects/' + project + '/displays.json')):
        print('static/projects/' + project + '/displays.json')
        with open('static/projects/' + project + '/displays.json') as points_file:
            displays = json.load(points_file)

        for display in displays:

            if display['video'] == True:
                x1 = display['points'][0]['x']
                x2 = display['points'][1]['x']
                y1 = display['points'][0]['y']
                y2 = display['points'][2]['y']
                w = x2 - x1
                h = y2 - y1

        for display in displays:
            width = float(display['width'])
            height = float(display['height'])

            ps = []

            for point in display['points']:
                ox = float(point['x'])
                oy = float(point['y'])
                x = (ox - x1) * width / w;
                y = (oy - y1) * height / h;
                ps.append([x, y])

            if display['video'] != True:
                frontCoverPtsBefore = np.array(ps, dtype="float32")
                frontCoverPtsAfter = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
                                              dtype="float32")

                # proc1 = Process(target=video_player, args=('video:' + str(display['port']), frontCoverPtsAfter, frontCoverPtsBefore, int(width), int(height)))
                # proc1.start()

        global proc1
        proc1 = Process(target=tr.video_player, args=(displays, run,)) #'video:' + str(display['port']), frontCoverPtsAfter, frontCoverPtsBefore, int(width), int(height)))
        run.value = 1.0
        proc1.start()


        # global player
        # player = MediaPlayer('3.a.mp4')

    return "Ok"

@app.route('/stop-video')
def stop_video():
    # proc1.terminate()
    run.value = 0.0
    return "Ok"


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'files'
#    app.run(host='0.0.0.0', port=5555)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5555)



