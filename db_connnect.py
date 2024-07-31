import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Session, declarative_base, relationship

base = declarative_base()

class Songs(base):
	__tablename__ = 'songs'
	ind = Column(Integer, primary_key=True)
	song_name = Column(String)
	genre = Column(String)

class Users(base):
	__tablename__ = 'users'
	email = Column(String, primary_key=True)
	username = Column(String)
	passw = Column(String)

engine = create_engine('sqlite:///./static/db/music_player.sqlite3')

def table_update(name, em, pswd):
	with engine.connect as u:
		s = insert(Users).values(email = em, username = name, passw = pswd)
		temp = u.execute(s)
		u.commit()


if __name__=='__main__':
	s = select(Songs)
	with engine.connect() as conn:
		data = conn.execute(s)
		for i in data:
			print(i)

	with Session(engine) as ses:
		song_list = ses.query(Songs).all()
		for i in song_list:
			print(i.ind,'-',i.song_name,'-',i.genre)