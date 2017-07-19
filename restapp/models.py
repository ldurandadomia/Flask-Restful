from restapp import db
from sqlalchemy.orm import synonym


class Switches(db.Model):
    """attributs d'un switch de l'infrastructure"""
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64), index=True, unique=False)
    ManagementIP = db.Column(db.String(20), index=True, unique=False)
    Ports = db.relationship('Ports', backref='SwitchNode', lazy='dynamic')

    Switch_Id = synonym("Id")

    def __repr__(self):
        return "Switch: Id={}, Name={}, ManagementIP={}".format(self.Id, self.Name, self.ManagementIP)

    def __getstate__(self):
        my_switch = {'Id': self.Id, 'Name': self.Name, 'ManagementIP': self.ManagementIP}
        return my_switch

    def GetAllAttributes(self):
        """ utilise par la version V1 des API """
        return self.__getstate__()


class Ports(db.Model):
    """attributs des ports d'un switch de l'infrastructure"""
    Id = db.Column(db.Integer, primary_key=True)
    Switch_Id = db.Column(db.Integer, db.ForeignKey('switches.Id'))
    Name = db.Column(db.String(64), index=True, unique=False)
    Speed = db.Column(db.String(8), index=True, unique=False)
    Duplex = db.Column(db.String(8), index=True, unique=False)
    Status = db.Column(db.String(8), index=True, unique=False)

    Port_Id = synonym("Id")

    def __repr__(self):
        return "Port: Id={}, Switch_Id={}, Name={}, Speed={}, Duplex={}, Status={}".format(self.Id,
         self.Switch_Id, self.Name, self.Speed, self.Duplex, self.Status)

    def __getstate__(self):
        my_port = {'Port_Id': self.Id, 'Switch_Id': self.Switch_Id, 'Name': self.Name, 'Speed': self.Speed,
             'Duplex': self.Duplex,
             'Status': self.Status}
        return my_port

    def GetAllAttributes(self):
        """utilise par la version V1 des API"""
        return self.__getstate__()

