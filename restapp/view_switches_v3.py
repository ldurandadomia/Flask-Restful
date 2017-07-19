from restapp import api
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from restapp import db, models
from view_common_v3 import switch_fields


class SetOfSwitches_v3(Resource):

    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('ManagementIP', type=str, required=True,
                                   help='No Management provided',
                                   location='json')
        self.post_parser.add_argument('Name', type=str, default="no name",
                                   location='json')

        super(SetOfSwitches_v3, self).__init__()


    @marshal_with(switch_fields, envelope='Switches')
    def get(self):
        """affiche tous les switchs de l'infrastructure ainsi que leurs ports"""
        try:
            dbSwitches = models.Switches.query.all()
        except:
            abort(400)
        if dbSwitches == None:
            abort(404)
        return dbSwitches


    @marshal_with(switch_fields, envelope='Switch')
    def post(self):
        """ajoute un switch a l'infrastructure"""
        args = self.post_parser.parse_args()
        try:
            un_switch = models.Switches(Name=args.Name, ManagementIP=args.ManagementIP)
            db.session.add(un_switch)
            db.session.commit()
        except:
            abort(400)
        return un_switch, 201


api.add_resource(SetOfSwitches_v3, '/todo/api/v3.0/Switches', endpoint='Switches_v3')