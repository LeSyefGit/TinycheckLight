from tinycheckweb import db

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    captures = db.relationship('Capture', backref='user',lazy=True)

    def __repr__(self):
        return self.email


class Capture(db.Model):
    __tablename__="captures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.name

class IOC(db.Model):
    __tablename__="iocs"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    tlp = db.Column(db.Text, nullable=False)
    tag = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    added_on = db.Column(db.Numeric, nullable=False)


class Whitelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.Text, nullable=False, unique=True)
    type = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    added_on = db.Column(db.Integer, nullable=False)