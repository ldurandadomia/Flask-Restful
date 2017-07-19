from restapp import api
from flask import jsonify
from flask import abort
from flask_restful import Resource, reqparse, fields, marshal
from restapp import db, models



class SingleSwitch(Resource):
    port_fields = {
        'Name': fields.String,
        'Speed': fields.String,
        'Duplex': fields.String,
        'Status': fields.String,
        'uri': fields.Url('Port', absolute=True, scheme='http'),
    }

    switch_fields = {
         'ManagementIP': fields.String,
         'Name': fields.String,
         'uri': fields.Url('Switch', absolute=True, scheme='http'),
                 'Ports': fields.List(fields.Nested(port_fields))
    }

    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('ManagementIP', type=str,
                                   location='json')
        self.put_parser.add_argument('Name', type=str,
                                   location='json')
        super(SingleSwitch, self).__init__()


    def get(self, Id):
        """affiche un switch de l'infrastructure ainsi que ses ports
        Le parametre Id doit correspondre au parametre defini :
            dans l'URL : /todo/api/v2.0/Switches/<int:Id>
            et a un attribut du modele de donnees : Id = db.Column(db.Integer, primary_key=True)
        """
        try:
            Switch = models.Switches.query.get(Id)
        except:
            abort(400)
        if Switch == None:
            abort(404)
        return {'Switch': marshal(Switch, SingleSwitch.switch_fields)}


    def put(self, Id):
        """modifie un switch de l'infrastructure"""
        try:
            Switch = models.Switches.query.get(Id)
        except:
            abort(400)
        if Switch == None:
            abort(404)
        args = self.put_parser.parse_args()

        if (args.Name != None):
            Switch.Name = args.Name
        if (args.ManagementIP != None):
            Switch.ManagementIP = args.ManagementIP
        try:
            db.session.commit()
        except:
            abort(400)
        return {'Switch': marshal(Switch, SingleSwitch.switch_fields)}


    def delete(self, Id):
        """supprime un switch de l'infrastructure ainsi que ses ports"""
        try:
            AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=Id).all()
            for port in AllSwitchPorts:
                db.session.delete(port)
            Switch = models.Switches.query.get(Id)
            db.session.delete(Switch)
            db.session.commit()
        except:
            abort(400)
        return jsonify({'result': True})

api.add_resource(SingleSwitch, '/todo/api/v2.0/Switches/<int:Id>', endpoint='Switch')