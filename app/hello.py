from flask import Flask

app = Flask(__name__)


@app.route("/")
def route_transit():
    return '<h1>Hello World</h1>'


@app.route("/test")
def func1():
    return '<h1>Hello World on test</h1>'


app.run(debug=True, host='localhost', port=80)


