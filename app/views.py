from app import app
from flask import render_template, request, url_for, redirect, session
import pykovtext

app.config.update(SECRET_KEY='swag')

def generateFiction(filetext):
	# send text file for text generation, currently only HP
	textfile = filetext + ".txt"

	file = open(textfile)
	# generate text via pykovtext module
	textgen = pykovtext.Pykvtxt(file,filetext)

	text = ''
	while len(text) < 250:
		tempText = textgen.printText(250)
		text = text + tempText + ' '
		
	text2 = ''
	while len(text2) < 250:
		tempText = textgen.printText(250)
		text2 = text2 + tempText + ' '

	file.close()
	print("Fiction Generated.")
	return text, text2

# Generate and display fan fiction method
@app.route('/generate')
def generate():
	# grab values from index.html
	fict1 = session.get('fict1', None)
	fict2 = session.get('fict2', None)

	fictions = {"hp" : "Harry Potter",
					"fnaf" : "Five Nights at Freddy's",
					"sonic" : "Sonic",
					"pkmn" : "Pokemon"}


	if fict1 == fict2:
		fanFic1, fanFic2 = generateFiction(fict1)
		return render_template('generate.html', title='Fancfiction Generator',fic1=fictions[fict1], gText=fanFic1, gText2=fanFic2)
	else:
		ffic = fictions[fict1] + " and " + fictions[fict2]

		if fict1 == "pkmn":
			if fict2 == "hp":
				fict1 = "hppkmn"
		elif fict1 == "sonic":
			if fict2 == "hp":
				fict1 = "hpsonic"
			elif fict2 == "pkmn":
				fict1 = "pkmnsonic"
		elif fict1 == "fnaf":
			if fict2 == "hp":
				fict1 = "hpfnaf"
			elif fict2 == "sonic":
				fict1 == "sonicfnaf"
			elif fict2 == "pkmn":
				fict1 = "pkmnfnaf"
		else:
			fict1 = fict1 + fict2

		# send it all to the web page to be displayed
		fanFic1, fanFic2 = generateFiction(fict1)
		return render_template('generate.html', title='Fancfiction Generator',fic1=ffic, gText=fanFic1, gText2=fanFic2)

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