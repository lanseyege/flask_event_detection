from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/about')
def about():
    return 'the about page'

@app.route('/projects/')
def projects():
    return 'the project page'

if __name__ == '__main__':
    app.run()

