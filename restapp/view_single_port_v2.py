from restapp import api
from flask import jsonify
from flask import abort
from flask_restful import Resource, reqparse, marshal
from restapp import db, models
from view_single_switch_v2 import SingleSwitch

class SinglePort(Resource):

    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('Name', type=str)
        self.put_parser.add_argument('Speed', type=str)
        self.put_parser.add_argument('Duplex', type=str)
        self.put_parser.add_argument('Status', type=str)
        super(SinglePort, self).__init__()


    def get(self, Switch_Id, Id):
        """affiche un des ports d'un switch de l'infrastructure"""
        try:
            Port = models.Ports.query.get(Id)
        except:
            abort(400)
        if Port == None:
            abort(404)
        if Port.Switch_Id != Switch_Id:
            abort(400)
        return {'Port': marshal(Port, SingleSwitch.port_fields)}


    def put(self, Switch_Id, Id):
        """modifie un port d'un switch de l'infrastructure"""
        try:
            Port = models.Ports.query.get(Id)
        except:
            abort(400)
        if Port == None:
            abort(404)
        if Port.Switch_Id != Switch_Id:
            abort(400)

        args = self.put_parser.parse_args()
        if (args.Name != None):
            Port.Name = args.Name
        if (args.Speed != None):
            Port.Speed = args.Speed
        if (args.Duplex != None):
            Port.Duplex = args.Duplex
        if (args.Status != None):
            Port.Status = args.Status

        try:
            db.session.commit()
        except:
            abort(400)
        return {'Port': marshal(Port, SingleSwitch.port_fields)}


    def delete(self, Switch_Id, Id):
        """supprime un port d'un switch de l'infrastructure"""
        try:
            Port = models.Ports.query.get(Id)
            if Port == None:
                abort(404)
            if Port.Switch_Id != Switch_Id:
                abort(400)
            db.session.delete(Port)
            db.session.commit()
        except:
            abort(400)
        return jsonify({'result': True})



api.add_resource(SinglePort, '/todo/api/v2.0/Switches/<int:Switch_Id>/Ports/<int:Id>', endpoint='Port')