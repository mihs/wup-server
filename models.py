from database import db

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20))
  token = db.Column(db.String(32))
  shared_entries = db.relationship('SharedFile', backref='user')

  def __init__(self, name, token):
    self.name = name
    self.token = token

  def __str__(self):
    return self.name

  def __repr__(self):
    return '<id: {0}, name: {1}>'.format(self.id, self.name)

class SharedFile(db.Model):
  __tablename__ = 'shared_files'

  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(100))
  filename = db.Column(db.String())

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __init__(self, uid, filename, user):
    self.uid = uid
    self.filename = filename
    self.user = user

  def __repr__(self):
    return '<id: {0}, filename: {1}, uid: {2}>'.format(self.id, self.filename, self.uid)
