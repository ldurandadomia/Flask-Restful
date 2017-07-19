from authapp import api
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from authapp import db, models
from view_common import object_fields


class Objects(Resource):

    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('Id', type=int, required=True,
                                   help='No object Id provided',
                                   location='json')
        self.post_parser.add_argument('Name', type=str, required=True,
                                   help='No object Name provided',
                                   location='json')

        super(Objects, self).__init__()


    @marshal_with(object_fields, envelope='Objects')
    def get(self):
        """affiche tous les objects de la base d'authorization ainsi que les regles associees"""
        try:
            AllObjects = models.Objects.query.all()
        except:
            abort(400)
        if AllObjects == None:
            abort(404)
        return AllObjects


    @marshal_with(object_fields, envelope='Object')
    def post(self):
        """ajoute un object a la base des authorization"""
        args = self.post_parser.parse_args()
        try:
            un_object = models.Objects(Name=args.Name, Id=args.Id)
            db.session.add(un_object)
            db.session.commit()
        except:
            abort(400)
        return un_object, 201


api.add_resource(Objects, '/todo/aaa/v1.0/Objects', endpoint='Objects')