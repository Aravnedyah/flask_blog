from flask import Flask

app = Flask(__name__)

#decorator creates flask view
@app.route('/')
def hello():
    return "hello world!"