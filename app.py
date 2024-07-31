from flask import Flask, request, render_template
import os
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base, relationship

base = declarative_base()

engine = create_engine('sqlite:///./static/db/music_player.sqlite3')

app = Flask(__name__)

app.config['UP_FOLDER'] = os.path.join('static')
app.config['SECRET_KEY'] = 'thisisMusiqApp'

users_list = []
pswd_list = []
email_list = []

song_list = ['Bad Liar','Enemy','Fairytale','Genius', 'Finish Line','Impossible','Middle of the Night','Paradise City', 'Peaky blinder', 'Born for This', 'The Search','Thunder','Unstoppable']
song_list.sort()

@app.route('/') 
def first():
	return render_template('index.html')

@app.route('/register',methods=['GET', 'POST'])
def reg():
	if request.method=="GET":
		return render_template('reg.html')
	if request.method=="POST":
		name = request.form['usrname']
		eml = request.form['email']
		pwsd = request.form['pwsd']
		rpwsd = request.form['rpwsd']
		if pwsd == rpwsd:
			users_list.append(name)
			pswd_list.append(pwsd)
			email_list.append(eml)
			return '<h1> Registration Successful , <a href="/login"> Login Again </a> </h1>'


@app.route('/login',methods=['GET', 'POST'])
def log_in():
	if request.method=="GET":
		return render_template('login.html')
	if request.method=="POST":
		username = request.form["usrname"]
		password = request.form["pwsd"]
		if password in pswd_list and username in users_list:
			return redirect(url_for('.uhome'))
		else:
			return '<h1> The Username or Password didn\'t match with the record , <a href="/login"> Try Again </a> </h1>'

@app.route('/admin-login',methods=['GET','POST'])
def admin_log_in():
	return render_template('adlog.html')

@app.route('/user-home', methods=['GET', 'POST'])
def uhome():
	if request.method == "GET":
		return render_template('uhome.html', song_list=song_list)
	if 'recommendation' in request:
		return redirect(url_for('reccomend'))
	if 'song' in request:
		song_name = request.form["song_name"]
		return redirect(url_for('song_page', song_name=song_name))

@app.route('/song/<song_name>',methods=['GET', 'POST'])
def song_page(song_name):
	pth = os.path.join('static','Lyrics')
	song = song_name+'.txt'
	file = open(os.path.join(pth,song), 'r')
	lyrics = file.readlines()
	return render_template('song_page.html',lyrics =  lyrics,song_name = song_name)

@app.route('/recommendation', methods=['GET','POST'])
def reccomend():
	if request.method=='GET':
		return render_template('recommendation.html',song_list = song_list)
	if request.method == 'POST':
		song_name = request.form["song_name"]
		return redirect(url_for('song_page', song_name=song_name))

@app.route('/all-songs')
def all_song():
	return render_template('allsongs.html',song_list=song_list)


app.run(debug=True)