from flask import Flask, render_template, request, session, redirect
import os
import json
import time
import cv2
import numpy as np
from multiprocessing import Process, Value

import translation as tr

app = Flask(__name__)
app.secret_key = "super secret key"
run = Value('d', 1.0)


@app.route('/')
def index():
    scene = ""
    video = ""

    if session.get('project') is None:
        session['project'] = 'demo'

    project = session.get('project')

    if os.path.exists('static/projects/' + project + '/scene/scene.jpg'):
        scene = '/static/projects/' + project + '/scene/scene.jpg'

        if os.path.exists('static/projects/' + project + '/video/small.jpg'):
            video = '/static/projects/' + project + '/video/small.jpg'

    with open('files/projects.json') as json_file:
        video_projects = json.load(json_file)

    return render_template('main.html', project=project, scene=scene, video=video, projects=video_projects)


@app.route('/projects', methods=['GET'])
def projects():
    with open('files/projects.json') as json_file:
        data = json.load(json_file)
        return data


@app.route('/content', methods=['POST', 'GET'])
def content():
    if request.method == "POST":
        data = request.get_json()

        if "project" in data:
            tmp = data.get('project')

            if tmp != 'Undefined':
                session['project'] = data['project']
                project = data['project']
                if not os.path.exists('static/projects/' + project):
                    os.mkdir('static/projects/' + project)
                    os.mkdir('static/projects/' + project + '/scene')
                    os.mkdir('static/projects/' + project + '/video')

    scene = ""
    video = ""
    project = session.get('project')

    if os.path.exists('static/projects/' + project + '/scene/scene.jpg'):
        scene = '/static/projects/' + project + '/scene/scene.jpg'

    if os.path.exists('static/projects/' + project + '/video/small.jpg'):
        video = '/static/projects/' + project + '/video/small.jpg'

    return render_template('content.html', project=session['project'], scene=scene, video=video)


@app.route('/upload')
def upload_html():
    path = request.args.get('path')
    return render_template('upload.html', path=path)


@app.route('/add')
def add_project():
    name = request.args.get('name')
    with open('files/projects.json') as json_file:
        video_projects = json.load(json_file)
        element = {"name": name}
        exists = element in video_projects

        if not exists:
            video_projects.append(element)
            print(video_projects)

            with open('files/projects.json', 'w') as outfile:
                json.dump(video_projects, outfile)
                session['project'] = name

                if not os.path.exists('static/projects/' + name):
                    os.mkdir('static/projects/' + name)
                    os.mkdir('static/projects/' + name + '/scene')
                    os.mkdir('static/projects/' + name + '/video')

    return redirect('/')


@app.route('/points', methods=['POST'])
def points():
    project = session['project']
    displays = request.get_json()

    with open('static/projects/' + project + '/displays.json', 'w') as outfile:
        json.dump(displays, outfile)
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

    if os.path.exists('static/projects/' + project + '/scene/scene.jpg'):
        os.remove("static/projects/" + project + "/scene/scene.jpg")

    if os.path.exists('static/projects/' + project + '/video/small.jpg'):
        os.remove("static/projects/" + project + "/video/small.jpg")
    if os.path.exists('static/projects/' + project + '/video/original.jpg'):
        os.remove("static/projects/" + project + "/video/original.jpg")
    if os.path.exists('static/projects/' + project + '/video/video.mp4'):
        os.remove("static/projects/" + project + "/video/video.mp4")

    os.rmdir("static/projects/" + project + "/scene")
    os.rmdir("static/projects/" + project + "/video")
    os.rmdir("static/projects/" + project)

    with open('files/projects.json') as json_file:
        video_projects = json.load(json_file)

        video_projects.remove(element)
        with open('files/projects.json', 'w') as outfile:
            json.dump(video_projects, outfile)
            session['project'] = 'demo'

    session['project'] = 'demo'

    return redirect('/')


@app.route('/edit')
def edit():
    project = session.get('project')
    path = request.args.get('path')
    print("edit: " + path)
    displays = []

    if os.path.exists('static/projects/' + project + '/displays.json'):
        print('static/projects/' + project + '/displays.json')
        with open('static/projects/' + project + '/displays.json') as points_file:
            displays = json.load(points_file)

    print(displays)
    return render_template('canvas-viewer.html', path=path, project=project, points=displays)


@app.route('/remove')
def remove():
    project = session.get('project')
    path = request.args.get('path')

    if path.find("scene") != -1:
        if os.path.exists('static/projects/' + project + '/scene/scene.jpg'):
            os.remove("static/projects/" + project + "/scene/scene.jpg")

    if path.find("video") != -1:
        if os.path.exists('static/projects/' + project + '/video/small.jpg'):
            os.remove("static/projects/" + project + "/video/small.jpg")
        if os.path.exists('static/projects/' + project + '/video/original.jpg'):
            os.remove("static/projects/" + project + "/video/original.jpg")
        if os.path.exists('static/projects/' + project + '/video/video.mp4'):
            os.remove("static/projects/" + project + "/video/video.mp4")

    return redirect('/')


@app.route('/start-video')
def start_video():
    project = session.get('project')
    print('start video ' + project)

    if os.path.exists('static/projects/' + project + '/displays.json'):
        print('static/projects/' + project + '/displays.json')
        with open('static/projects/' + project + '/displays.json') as points_file:
            displays = json.load(points_file)

        x1 = 0
        y1 = 0
        w = 0
        h = 0

        for display in displays:

            if display['video']:
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
                x = (ox - x1) * width / w
                y = (oy - y1) * height / h
                ps.append([x, y])

        proc1 = Process(target=tr.video_player, args=(displays, run, project,))
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
