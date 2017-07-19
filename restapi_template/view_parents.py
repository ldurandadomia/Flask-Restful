from <module> import api
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from <module> import db, models
from view_common import parent_fields


class SetOfParents(Resource):

    def __init__(self):
        """Constructor: HTML body fields parsing"""
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('<Attribute1>', type=str, required=True,
                                   help='No <Attribute1> provided',
                                   location='json')
        self.post_parser.add_argument('<Attribute2>', type=str, default="no value",
                                   location='json')
        ...
        self.post_parser.add_argument('<AttributeN>', type=str, default="no value",
                                      location='json')
        super(SetOfParents, self).__init__()


    @marshal_with(parent_fields, envelope='parents')
    def get(self):
        """display all parents elements in SetOfParents"""
        try:
            dbParents = models.parents.query.all()
        except:
            abort(400)
        if dbParents == None:
            abort(404)
        return dbParents


    @marshal_with(parent_fields, envelope='parent')
    def post(self):
        """add a parent to the collection SetOfParents"""
        args = self.post_parser.parse_args()
        try:
            aparent = models.parents(<Attribute1>=args.<Attribute1>, <Attribute2>=args.<Attribute2>, … ,
                                     <AttributeN>=args.<AttributeN>)
            db.session.add(aparent)

            # process parent node creation on physical infrastructure
            success = self.create(args)
            if success == True:
                db.session.commit()
                return aparent, 201
            if success == False:
                db.session.rollback()
                abort(400)
        except:
            abort(400)


    def create(self, args):
        """process a parent creation onto the physical infrastructure"""

        # put real node creation instruction here
        # return True if creation is successful else False
        return True


api.add_resource(SetOfParents, '/api/v1.0/parents', endpoint='parents')
