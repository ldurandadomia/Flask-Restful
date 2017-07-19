from <module> import api
from flask import jsonify
from flask import abort
from flask_restful import Resource, reqparse, marshal_with
from <module> import db, models
from view_common import child_fields


class SingleChild(Resource):

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
        super(SingleChild, self).__init__()


    @marshal_with(child_fields, envelope='child')
    def get(self, parent_id, id):
        """display a child of a given parent"""
        achild = models.childs.query.get_or_404(id)
        if achild.parent_id != parent_id:
            abort(400)
        return achild 


    @marshal_with(child_fields, envelope='child')
    def put(self, parent_id, id):
        """update a child of a given parent"""
        achild = models.childs.query.get_or_404(id)
        if achild.parent_id != parent_id:
            abort(400)
        args = self.put_parser.parse_args()
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in ["<Attribute1>", "<Attribute2>", …, "<AttributeN>"]:
            setattr(achild, attribut, IfUpdated(getattr(args, attribut), getattr(achild, attribut)))
        # process parent node update on physical infrastructure
        success = self.update(args)
        if success == True:
            db.session.commit()
            return achild
        if success == False:
            db.session.rollback()
            abort(400)

    def delete(self, parent_id, id):
        """remove a child of a given parent"""
        achild = models.childs.query.get_or_404(id)
        if achild.parent_id != parent_id:
            abort(400)
        db.session.delete(achild)
        # process child node deletion on physical infrastructure
        success = self.remove(...)
        if success == True:
            db.session.commit()
            return jsonify({'result': True})
        if success == False:
            db.session.rollback()
            abort(400)

    def update(self, args):
        """process a child node configuration update onto the physical infrastructure"""
        # put real node update instructions here
        # return True if update is successful else False
        return True

    def remove(self, …):
        """process a child node configuration deletion onto the physical infrastructure"""
        # put real node delete instructions here
        # return True if delete is successful else False
        return True


api.add_resource(SingleChild, '/api/v1.0/parents/<int:parent_id>/childs/<int:id>', endpoint='child')
