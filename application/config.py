from application import envs

class Config(object):
    SQLALCHEMY_DATABASE_URI = envs.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SECRET_KEY = envs.SECRET_KEY