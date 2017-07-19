from <module> import api
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from <module> import db, models
from view_common import child_fields


class SetOfChilds(Resource):
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
        super(SetOfChilds, self).__init__()


    @marshal_with(child_fields, envelope='childs')
    def get(self, parent_id):
        """display all childs of a given parent"""
        try:
            AllChilds = models.childs.query.filter_by(parent_id=parent_id).all()
        except:
            abort(400)
        if AllChilds == None:
            abort(404)
        return AllChilds


    @marshal_with(child_fields, envelope='child')
    def post(self, parent_id):
        """add a new child to a given parent"""
        args = self.post_parser.parse_args()
        try:
            aparent = models.parents.query.get(parent_id)
        except:
            abort(400)
        if aparent == None:
            abort(404)
        try:
            achild = models.childs(<Attribute1>=args.<Attribute1>, <Attribute2>=args.<Attribute2>, … ,
                                 <AttributeN>=args.<AttributeN>)
            db.session.add(achild)
            # process child node creation on physical infrastructure
            success = self.create(args)
            if success == True:
                db.session.commit()
                return achild, 201
            if success == False:
                db.session.rollback()
                abort(400)
        except:
            abort(400)

        def create(self, args):
            """process a child node creation onto the physical infrastructure"""
            # put real node creation instruction here
            # return True if creation is successful else False
            return True

api.add_resource(SetOfPorts, '/api/v1.0/parents/<int:parent_id>/childs', endpoint=childs')