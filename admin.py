from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page - goto <a href='/hello'>hello</a>"

@app.route('/hello')
def hello():
    return "Hello World - goto <a href='/upload'>upload</a>"


@app.route('/upload')
def upload_html():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('files/' + f.filename)
        return 'file uploaded successfully'

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'files'
    app.run(host='0.0.0.0', port=5555)