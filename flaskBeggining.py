from flask import Flask,request
from markupsafe import escape
app = Flask(__name__)
@app.route('/')
def hello():
    name = request.args.get('name','Flask')
    return f"Hello, {escape(name)}!"

@app.route('/<username>')
def hello_name(username):
     return f"Hello, {escape(username)}!"



if __name__ ==  '__main__':
    app.run(debug=True)

