from restapp import api
from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from restapp import db, models
from view_common_v3 import switch_fields


class SingleSwitch_v3(Resource):
    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('ManagementIP', type=str,
                                     location='json')
        self.put_parser.add_argument('Name', type=str,
                                     location='json')
        super(SingleSwitch_v3, self).__init__()

    @marshal_with(switch_fields, envelope='Switch')
    def get(self, Id):
        """affiche un switch de l'infrastructure ainsi que ses ports
        Le parametre Id doit correspondre au parametre defini :
            dans l'URL : /todo/api/v3.0/Switches/<int:Id>
            et a un attribut du modele de donnees : Id = db.Column(db.Integer, primary_key=True)
        """
        # Si la recherche est infructueuse une exception sera emise
        # les exceptions 400, 500 sont interceptees par l'API restful
        # l'exception 404 est interceptee uniquement si catch_all_404s=True est positionne
        # lors de l'instanciation de l'API
        Switch = models.Switches.query.get_or_404(Id)
        return Switch

    @marshal_with(switch_fields, envelope='Switch')
    def put(self, Id):
        """modifie un switch de l'infrastructure"""
        Switch = models.Switches.query.get_or_404(Id)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["Name", "ManagementIP"]:
            setattr(Switch, attribut, IfUpdated(getattr(args, attribut), getattr(Switch, attribut)))
        db.session.commit()
        return Switch

    def delete(self, Id):
        """supprime un switch de l'infrastructure ainsi que ses ports"""
        AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=Id).all()
        for port in AllSwitchPorts:
            db.session.delete(port)
        Switch = models.Switches.query.get_or_404(Id)
        db.session.delete(Switch)
        db.session.commit()
        return jsonify({'result': True})


api.add_resource(SingleSwitch_v3, '/todo/api/v3.0/Switches/<int:Id>', endpoint='Switch_v3')
