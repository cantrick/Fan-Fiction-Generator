from app import app
from flask import render_template, request, url_for, redirect, session
import pykovtext

app.config.update(SECRET_KEY='swag')

# Generate and display fan fiction method
@app.route('/generate')
def generate():
	# grab values from index.html
	fict1 = session.get('fict1', None)
	fict2 = session.get('fict2', None)

	# send text file for text generation, currently only HP
	file = open("hp.txt")
	# generate text via pykovtext module
	textgen = pykovtext.Pykvtxt(file)
	# send it all to the web page to be displayed
	return render_template('generate.html', title='Fancfiction Generator',fic1=fict1, fic2=fict2, gText=textgen.printText(250))

# Main page method
@app.route('/')
@app.route('/index', methods = ['POST', 'GET'])
def index():
	# get title and values from dropdowns
	# send values after the submit button is pressed
	title = "Fanfiction GEnerator"
	if request.method == 'POST':
		# get session values from the web page dropdowns
		session['fict1'] = request.form.get('sel1')
		session['fict2'] = request.form.get('sel2')
		# go to the generate.html page
		return redirect(url_for('generate'))

	return render_template('index.html', title=title)