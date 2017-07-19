from flask import jsonify
from flask import abort
from flask_restful import Resource, marshal
from restapp import db


class RestDataElement(Resource):
    """ Single element from RestDataCollection:
    Manage with REST a single element of a RestDataCollection :
        - GET : is allowing to display one given element of the collection
        - PUT : is allowing to modify one given element of the collection
        - DELETE : is allowing to delete one given element of the collection
    """

    def __init__(self, **kwargs):
        """ RestDataElement collection element constructor:
        - Database : SQL database which is containing table
        - Table : data persistence table
        - SingleElementTitle : JSON title to display for a single element display
        - DisplayFormat : JSON list of fields to be displayed when a GET is issued
        - PutParser : JSON list of fields to be parsed when a PUT is received
        - ParentKey (optional) : ParentKey name in Child object model
        - ChildTable : child data peristence table
        """
        super(RestDataElement, self).__init__()
        self.Database = kwargs['Database']
        self.dbTable = kwargs['Table']
        self.Key = kwargs['Key']
        self.SingleElementTitle = kwargs['SingleElementTitle']
        self.DisplayFormat = kwargs['DisplayFormat']
        self.PutParser = kwargs['PutParser']

        self.has_parent = False
        if kwargs.has_key('ParentKey'):
            self.has_parent = True
            self.ParentKey = kwargs['ParentKey']

        self.has_child = False
        if kwargs.has_key('ChildParentKey'):
            self.has_child = True
            self.ChildParentKey = kwargs['ChildParentKey']
            self.dbChildTable =  kwargs['ChildTable']


    def get(self, **kwargs):
        """ display a single element.
        self.Key is the element key provided into the api URL.
        self.ParentKey (optional) : is the foreign key of parent node provided into the api URL
        """
        Key = kwargs[self.Key]
        # Parent or Child Ressource
        OneElement = self.dbTable.query.get_or_404(Key)

        if self.has_parent:
            ParentKeyValue = kwargs.get(self.ParentKey)
            if getattr(OneElement, self.ParentKey) != ParentKeyValue:
                abort(404)
        return marshal(OneElement, self.DisplayFormat, self.SingleElementTitle), 200


    def put(self, **kwargs):
        """ update a single element.
        self.Key is the element key provided into the api URL.
        self.ParentKey (optional) : is the foreign key of parent node provided into the api URL
        """
        Key = kwargs[self.Key]
        # Parent or Child Ressource
        OneElement = self.dbTable.query.get_or_404(Key)

        if self.has_parent:
            ParentKeyValue = kwargs.get(self.ParentKey)
            if getattr(OneElement, self.ParentKey) != ParentKeyValue:
                abort(404)

        args = self.PutParser.parse_args()
        argdict = dict(args)
        IfUpdated = lambda x, y: y if x is None else x
        for attribut in argdict.keys():
            setattr(OneElement, attribut, IfUpdated(getattr(args, attribut), getattr(OneElement, attribut)))
        self.Database.session.commit()
        return marshal(OneElement, self.DisplayFormat, self.SingleElementTitle), 200


    def delete(self, **kwargs):
        """ remove a single element.
        self.Key is the element key provided into the api URL.
        self.ParentKey (optional) : is the foreign key of parent node provided into the api URL
        """
        # Delete Child resources bound to a Parent
        if self.has_child:
            KeyValue = kwargs.get(self.Key)
            dbQuery = self.dbChildTable.query
            dbQuery = dbQuery.filter(getattr(self.dbChildTable, self.ChildParentKey) == KeyValue)
            AllChildElements = dbQuery.all()
            for Element in AllChildElements:
                db.session.delete(Element)

        # Delete a Parent or a Child resource
        Key = kwargs[self.Key]
        OneElement = self.dbTable.query.get_or_404(Key)

        if self.has_parent:
            ParentKeyValue = kwargs.get(self.ParentKey)
            if getattr(OneElement, self.ParentKey) != ParentKeyValue:
                abort(404)

        db.session.delete(OneElement)
        db.session.commit()
        return jsonify({'result': True})