from authapp import api
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from authapp import db, models
from view_common import default_rule_fields
from flask import request

class DefaultRules(Resource):

    def __init__(self):
        """Constructeur: liste les champs attendus dans le corps HTML"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('Name', type=str, required=True,
                                      help='No rule object name provided',
                                      location='json')
        self.post_parser.add_argument('Method', type=str, required=True,
                                   help='No rule method provided',
                                   location='json')
        self.post_parser.add_argument('Role', type=str, required=True,
                                   help='No rule role provided',
                                   location='json')

        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('Name', type=str, required=True,
                                      help='No rule object name provided',
                                      location='json')
        self.get_parser.add_argument('Method', type=str, required=True,
                                   help='No rule method provided',
                                   location='json')

        super(DefaultRules, self).__init__()


    @marshal_with(default_rule_fields, envelope='Rules')
    def get(self):
        """affiche toutes les regles par defaut associees aux noms d'objets"""
        filter = False
        if request.data != '':
             filter = True
             args = self.get_parser.parse_args()
        try:
            if filter == False:
                AllRules = models.DefaultRules.query.all()
            else:
                AllRules = models.DefaultRules.query.filter_by(Name=args.Name, Method=args.Method).all()
        except:
            abort(400)
        if AllRules == None or len(AllRules)==0:
            abort(404)
        return AllRules


    @marshal_with(default_rule_fields, envelope='Rule')
    def post(self):
        """ajoute une regle par defaut a un nom d'objet"""
        args = self.post_parser.parse_args()
        try:
            une_rule = models.DefaultRules(Name=args.Name, Method=args.Method, Role=args.Role)
            db.session.add(une_rule)
            db.session.commit()
        except:
            abort(400)
        return une_rule, 201


api.add_resource(DefaultRules, '/todo/aaa/v1.0/DefaultRules', endpoint='DefaultRules')