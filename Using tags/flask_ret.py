from flask import Flask
from flask import *

app = Flask(__name__)

def hello_world():
    return 'test'

@app.route('/', methods=['GET', 'POST'])
def hello():
  print "\na\n"
  return hello_world()

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
