
from flask import request
from flask import Flask
from flask import url_for
from flask import render_template
import ast


app = Flask(__name__)

#@app.route('/')
#def my_form():
#  return render_template("\form.html")

@app.route("/", methods=['GET', 'POST'])
def hello():
  if request.method == 'POST':
    text= request.form.copy().keys()[0] # Wezkeug immutable multi dict
    print type(request.form.copy()) # Werkzeug Multidict
    print type(request.form.copy().keys()) # list
    text2= ast.literal_eval(text) # dict
    print type(text2) # dict
    print text2
    text3 = request.form.copy()
    print type(text3)
    #print text3.getlist('msg')
    print type(text3.items()[0][0])
    text4= ast.literal_eval(text3.items()[0][0]) # dict
    print type(text4)
    print text4
    print request.form# Immutable Multidict
    print request.form.copy()# Multidict
    for i in text4:
      print i
    return "H\n"
  else:
    index()
#text= raw_input('Enter text that you want to search: ')

def splitted(text):
  return text.split()

@app.route('/search')
def search():
  text= request.form['text']
  splitted = text.split()
  print splitted


@app.route('/index')
def index():
    return 'Index Page'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

with app.test_request_context():
  print url_for('index')
  print url_for('search')
  print url_for('about')
  print url_for('hello')


if __name__ == "__main__":
  app.debug=True
  app.run(host='0.0.0.0')
  # app.run(debug=True)
