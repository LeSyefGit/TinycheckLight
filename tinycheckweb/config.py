class Config:
    SECRET_KEY = 'ec6a68c37f8a50e5b13add8a636e6575'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tinycheck.sqlite3'
    JWT_SECRET_KEY = SECRET_KEY
    UPLOAD_FOLDER = '/medias/captures/'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
