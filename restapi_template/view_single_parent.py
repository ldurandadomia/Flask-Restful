from <module> import api
from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with
from <module> import db, models
from view_common import parent_fields


class SingleParent(Resource):
    def __init__(self):
        """Constructor: HTML body fields parsing"""
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('<Attribute1>', type=str, required=True,
                                   help='No <Attribute1> provided',
                                   location='json')
        self.put_parser.add_argument('<Attribute2>', type=str, default="no value",
                                   location='json')
        ...
        self.put_parser.add_argument('<AttributeN>', type=str, default="no value",
                                      location='json')
        super(SingleParent, self).__init__()

    @marshal_with(parent_fields, envelope='parent')
    def get(self, id):
        """display a given parent and all its childs"""
        aparent = models.parents.query.get_or_404(id)
        return aparent 

    @marshal_with(parent_fields, envelope='parent')
    def put(self, id):
        """update a given parent"""
        aparent = models.parents.query.get_or_404(id)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["<Attribute1>", "<Attribute2>", …, "<AttributeN>"]:
            setattr(aparent, attribut, IfUpdated(getattr(args, attribut), getattr(aparent, attribut)))
        # process parent node update on physical infrastructure
        success = self.update(args)
        if success == True:
            db.session.commit()
            return aparent
        if success == False:
            db.session.rollback()
            abort(400)

    def delete(self, id):
        """remove a given parent and all its childs"""
        AllChilds = models.childs.query.filter_by(parent_id=id).all()
        for child in AllChilds:
            db.session.delete(child)
         aparent = models.parents.query.get_or_404(id)
        db.session.delete(aparent)
        # process parent node deletion on physical infrastructure
        success = self.remove(...)
        if success == True:
            db.session.commit()
            return jsonify({'result': True})
        if success == False:
            db.session.rollback()
            abort(400)

    def update(self, args):
        """process a parent node configuration update onto the physical infrastructure"""
        # put real node update instructions here
        # return True if update is successful else False
        return True


    def remove(self, …):
        """process a parent node configuration delete onto the physical infrastructure"""
        # put real node delete instructions here
        # return True if delete is successful else False
        return True


api.add_resource(SingleParent, '/api/v1.0/parents/<int:id>', endpoint='parent')
