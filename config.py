import os

basedir = os.path.abspath(os.path.dirname(__file__))


# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'alayatodo.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repos')


# pagination
TODOS_PER_PAGE = 3