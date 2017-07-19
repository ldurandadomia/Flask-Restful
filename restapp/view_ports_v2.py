from restapp import api
from flask import abort
from flask_restful import Resource, reqparse, marshal
from restapp import db, models
from view_single_switch_v2 import SingleSwitch


class SetOfPorts(Resource):
    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('Name', type=str, required=True,
                                   help='No port name provided',
                                   location='json')
        self.post_parser.add_argument('Speed', type=str, default="1000",
                                   location='json')
        self.post_parser.add_argument('Duplex', type=str, default="full",
                                   location='json')
        self.post_parser.add_argument('Status', type=str, default="disable",
                                   location='json')
        super(SetOfPorts, self).__init__()


    def get(self, Switch_Id):
        """affiche tous les ports d'un switch de l'infrastructure"""
        try:
            AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=Switch_Id).all()
        except:
            abort(400)
        if AllSwitchPorts == None:
            abort(404)
        return {'Port': marshal(AllSwitchPorts, SingleSwitch.port_fields)}


    def post(self, Switch_Id):
        """ajoute un port a un switch a l'infrastructure"""
        args = self.post_parser.parse_args()
        try:
            un_switch = models.Switches.query.get(Switch_Id)
        except:
            abort(400)
        if un_switch == None:
            abort(404)
        try:
            un_port = models.Ports(Name=args.Name,
                                   Speed=args.Speed,
                                   Duplex=args.Duplex,
                                   Status=args.Status,
                                   SwitchNode=un_switch)
            db.session.add(un_port)
            db.session.commit()
        except:
            abort(400)
        return {'Port': marshal(un_port, SingleSwitch.port_fields)}, 201


api.add_resource(SetOfPorts, '/todo/api/v2.0/Switches/<int:Switch_Id>/Ports', endpoint='Ports')
