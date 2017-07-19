from <module> import db


class parents(db.Model):
    """parent attributes"""
    id = db.Column(db.Integer, primary_key=True)
    <Attribute1> = db.Column(db.String(64), index=True, unique=False)
    <Attribute2> = db.Column(db.String(64), index=True, unique=False)
    ...
    <AttributeN> = db.Column(db.String(64), index=True, unique=False)
    childs = db.relationship('childs', backref='child_node', lazy='dynamic')


class childs(db.Model):
    """child attributes"""
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    <Attribute1> = db.Column(db.String(64), index=True, unique=False)
    <Attribute2> = db.Column(db.String(64), index=True, unique=False)
    ...
    <AttributeN> = db.Column(db.String(64), index=True, unique=False)
