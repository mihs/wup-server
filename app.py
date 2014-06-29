import flask
from flask import Flask, jsonify, url_for, send_from_directory, request
import os
import uuid
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config.from_object(os.environ['APP_ENV'])
import database
database.init(app)
from database import db
import models

import logging
from logging import FileHandler
file_handler = FileHandler('./log/{0}'.format(os.environ['APP_ENV'].split('.')[1]))
file_handler.setLevel(app.config['LOG_LEVEL'])
app.logger.addHandler(file_handler)

@app.route('/', methods = ['POST'])
def new_shared_file():
  file = request.files['file']
  token = request.headers['X-Auth-Token']
  dbuser = models.User.query.filter_by(token = token).first()
  if dbuser == None:
    return jsonify(error='User is not registered'), 403
  if file == None:
    return jsonify(error='File not provided'), 400
  uid = uuid.uuid4().hex
  filename = secure_filename(file.filename)
  into_dir = os.path.join(app.config['UPLOAD_PATH'], str(dbuser.id), uid)
  os.makedirs(into_dir, mode = 0o750, exist_ok = True)
  file.save(os.path.join(into_dir, filename))
  shared_file = models.SharedFile(uid, filename, dbuser)
  db.session.add(shared_file)
  db.session.commit()
  return jsonify(url = url_for('send_shared_file', file_uid = uid, _external = True))

@app.route('/<file_uid>', methods = ['GET'])
def send_shared_file(file_uid):
  dbentry = models.SharedFile.query.filter_by(uid = file_uid).first_or_404()
  return send_from_directory(os.path.join(app.config['UPLOAD_PATH'], str(dbentry.user.id), file_uid), dbentry.filename, as_attachment = True, attachment_filename = dbentry.filename)

if __name__ == '__main__':
  app.run()
