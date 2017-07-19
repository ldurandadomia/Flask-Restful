from authapp import api
from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from authapp import db, models
from view_common import object_fields


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
        anObject = models.Objects.query.get_or_404(Uuid)
        return anObject

    @marshal_with(object_fields, envelope='Object')
    def put(self, Uuid):
        """modifie un object de la base des authorization"""
        anObject = models.Objects.query.get_or_404(Uuid)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["Name", "Id"]:
            setattr(anObject, attribut, IfUpdated(getattr(args, attribut), getattr(anObject, attribut)))
        db.session.commit()
        return anObject

    def delete(self, Uuid):
        """supprime un object ainsi que les regles associees"""
        AllRules = models.AuthorizationRules.query.filter_by(Uuid=Uuid).all()
        for rule in AllRules:
            db.session.delete(rule)
        anObject = models.Objects.query.get_or_404(Uuid)
        db.session.delete(anObject)
        db.session.commit()
        return jsonify({'result': True})


api.add_resource(Object, '/todo/aaa/v1.0/Objects/<int:Uuid>', endpoint='Object')