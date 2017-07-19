from authapp import api
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from authapp import db, models
from view_common import author_rule_fields


class AuthorizationRules(Resource):

    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('Method', type=str, required=True,
                                   help='No rule method provided',
                                   location='json')
        self.post_parser.add_argument('Role', type=str, required=True,
                                   help='No rule role provided',
                                   location='json')
        super(AuthorizationRules, self).__init__()


    @marshal_with(author_rule_fields, envelope='Rules')
    def get(self, Uuid):
        """affiche toutes les regles d'authorization"""
        try:
            AllRules = models.AuthorizationRules.query.filter_by(Uuid=Uuid).all()
        except:
            abort(400)
        if AllRules == None:
            abort(404)
        return AllRules


    @marshal_with(author_rule_fields, envelope='Rule')
    def post(self, Uuid):
        """ajoute une regle par d'authorization"""
        args = self.post_parser.parse_args()
        anObject = models.Objects.query.get_or_404(Uuid)
        try:
            une_rule = models.AuthorizationRules(Method=args.Method, Role=args.Role, Object=anObject)
            db.session.add(une_rule)
            db.session.commit()
        except:
            abort(400)
        return une_rule, 201


api.add_resource(AuthorizationRules, '/todo/aaa/v1.0/Objects/<int:Uuid>/AuthorizationRules', endpoint='AuthorizationRules')