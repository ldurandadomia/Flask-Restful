from restapp import api
from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from restapp import db, models
from view_common_v4 import object_fields


class Object(Resource):
    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('Id', type=int,
                                     location='json')
        self.put_parser.add_argument('Name', type=str,
                                     location='json')
        super(Object, self).__init__()

    @marshal_with(object_fields, envelope='Object')
    def get(self, Uuid):
        """affiche un object de la base des authorization"""
        Object = models.Objects.query.get_or_404(Uuid)
        return Object

    @marshal_with(object_fields, envelope='Object')
    def put(self, Uuid):
        """modifie un object de la base des authorization"""
        Object = models.Objects.query.get_or_404(Uuid)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["Name", "Id"]:
            setattr(Object, attribut, IfUpdated(getattr(args, attribut), getattr(Object, attribut)))
        db.session.commit()
        return Object

    def delete(self, Uuid):
        """supprime un object ainsi que les regles associees"""
        AllRules = models.AuthorizationRules.query.filter_by(Uuid=Uuid).all()
        for rule in AllRules:
            db.session.delete(rule)
        Object = models.Objects.query.get_or_404(Id)
        db.session.delete(Object)
        db.session.commit()
        return jsonify({'result': True})


api.add_resource(Object, '/todo/api/v4.0/Objects/<int:Uuid>', endpoint='Object')