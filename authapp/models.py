from authapp import db

class Objects(db.Model):
    """attributs des objets"""
    Uuid = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), index=True, unique=False)
    Id = db.Column(db.Integer, index=True, unique=False)
    Rules = db.relationship('AuthorizationRules', backref='Object', lazy='dynamic')

    def __init__(self, Name, Id):
        self.Name = Name
        self.Id = Id
        super(Objects, self).__init__()

    def __repr__(self):
        return "Object: Uuid={}, Name={}, Id={}".format(self.Uuid, self.Name, self.Id)

    def __getstate__(self):
        my_object = {'Uuid': self.Uuid, 'Name': self.Name, 'Id': self.Id}
        return my_object


class AuthorizationRules(db.Model):
    """Authorization"""
    __tablename__ = "authorizationrules"
    Id = db.Column(db.Integer, primary_key=True)
    Uuid = db.Column(db.Integer, db.ForeignKey('objects.Uuid'))
    Method = db.Column(db.String(64), index=True, unique=False)
    Role = db.Column(db.Integer, index=True, unique=False)

class DefaultRules(db.Model):
    """Default Authorization Rules"""
    __tablename__ = "defaultrules"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), index=True, unique=False)
    Method = db.Column(db.String(64), index=True, unique=False)
    Role = db.Column(db.Integer, index=True, unique=False)