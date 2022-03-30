from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page - goto <a href='/hello'>hello</a>"

@app.route('/hello')
def hello():
    return "Hello World - goto <a href='/'>main</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)