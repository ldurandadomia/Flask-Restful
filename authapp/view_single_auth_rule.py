from authapp import api
from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from authapp import db, models
from view_common import author_rule_fields


class AuthorizationRule(Resource):
    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('Method', type=str,
                                     location='json')
        self.put_parser.add_argument('Role', type=str,
                                     location='json')
        super(AuthorizationRule, self).__init__()

    @marshal_with(author_rule_fields, envelope='Rule')
    def get(self, Uuid, Id):
        """affiche une regle associee a un object de la base des authorization"""
        aRule = models.AuthorizationRules.query.get_or_404(Id)
        if aRule.Uuid != Uuid:
            abort(400)
        return aRule

    @marshal_with(author_rule_fields, envelope='Rule')
    def put(self, Uuid, Id):
        """modifie une regle par defaut de la base des authorization"""
        aRule = models.AuthorizationRules.query.get_or_404(Id)
        if aRule.Uuid != Uuid:
            abort(400)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["Method", "Role"]:
            setattr(aRule, attribut, IfUpdated(getattr(args, attribut), getattr(aRule, attribut)))
        db.session.commit()
        return aRule

    def delete(self, Uuid, Id):
        """supprime une regle par defaut"""
        aRule = models.AuthorizationRules.query.get_or_404(Id)
        if aRule.Uuid != Uuid:
            abort(400)
        db.session.delete(aRule)
        db.session.commit()
        return jsonify({'result': True})


api.add_resource(AuthorizationRule, '/todo/aaa/v1.0/Objects/<int:Uuid>/AuthorizationRules/<int:Id>', endpoint='AuthorizationRule')