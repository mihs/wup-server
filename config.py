import os
import logging

class all(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = '' # Add a secret key here

class production(all):
  DEBUG = False
  SERVER_NAME = 'share.ifnotnull.net'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None) or 'sqlite:////srv/cloud/wup/data.db'
  UPLOAD_PATH = '/srv/cloud/wup/share'
  SERVER_NAME = ''
  LOG_LEVEL = logging.ERROR

class staging(all):
  DEVELOPMENT = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None) or 'sqlite:///data.db'
  UPLOAD_PATH = './uploads'
  SERVER_NAME = ''
  LOG_LEVEL = logging.ERROR

class development(all):
  DEVELOPMENT = True
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None) or 'sqlite:///data.db'
  UPLOAD_PATH = './uploads'
  SERVER_NAME = 'localhost:3000'
  LOG_LEVEL = logging.DEBUG

class testing(all):
  TESTING = True
  LOG_LEVEL = logging.DEBUG
