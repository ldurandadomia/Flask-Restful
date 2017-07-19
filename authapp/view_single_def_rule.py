from authapp import api
from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from authapp import db, models
from view_common import default_rule_fields


class DefaultRule(Resource):
    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('Name', type=str,
                                     location='json')
        self.put_parser.add_argument('Method', type=str,
                                     location='json')
        self.put_parser.add_argument('Role', type=str,
                                     location='json')
        super(DefaultRule, self).__init__()

    @marshal_with(default_rule_fields, envelope='Rule')
    def get(self, Id):
        """affiche une regle par defaut de la base des authorization"""
        aRule = models.DefaultRules.query.get_or_404(Id)
        return aRule

    @marshal_with(default_rule_fields, envelope='Rule')
    def put(self, Id):
        """modifie une regle par defaut de la base des authorization"""
        aRule = models.DefaultRules.query.get_or_404(Id)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["Name", "Method", "Role"]:
            setattr(aRule, attribut, IfUpdated(getattr(args, attribut), getattr(aRule, attribut)))
        db.session.commit()
        return aRule

    def delete(self, Id):
        """supprime une regle par defaut"""
        AllRules = models.DefaultRules.query.filter_by(Id=Id).all()
        for rule in AllRules:
            db.session.delete(rule)
        aRule = models.DefaultRules.query.get_or_404(Id)
        db.session.delete(aRule)
        db.session.commit()
        return jsonify({'result': True})


api.add_resource(DefaultRule, '/todo/aaa/v1.0/DefaultRules/<int:Id>', endpoint='DefaultRule')