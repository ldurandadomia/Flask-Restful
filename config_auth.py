import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_auth.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository_auth')
