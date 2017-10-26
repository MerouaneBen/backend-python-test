from alayatodo import db

class Users(db.Model): 
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255),index=True,unique=True,nullable=False)
	password = db.Column(db.String(255),nullable=False)

	def __repr__(self):
		return '<Users %r>' % (self.username)

class Todos(db.Model): 
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,  db.ForeignKey('users.id'), nullable=False)
	description = db.Column(db.String(255),nullable=False)
	is_completed = db.Column(db.Boolean, unique=False, default=False)

	def __repr__(self):
		return '<Todos %r>' % (self.description)
