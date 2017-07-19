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
        self.ResourceModel = kwargs['RestResourceModel']

        # Parent Object Table Description
        self.Database = self.ResourceModel.Database
        self.dbTable = self.ResourceModel.Table
        self.Key = self.ResourceModel.Key
        self.SingleElementTitle = self.ResourceModel.SingleElementTitle
        self.DisplayFormat = self.ResourceModel.DisplayFormat
        self.PutParser = self.ResourceModel.PutParser

        self.has_parent = False
        self.Parents = self.ResourceModel.Parents
        if len(self.Parents) > 0:
            self.has_parent = True

        self.has_child = False
        self.Childs = self.ResourceModel.Childs
        if len(self.Childs) > 0:
            self.has_child = True


    def delete_all_childs(self, ChildList, ParentKeyValue):
        """Manage childs deletion for DELETE method applied on Parents"""
        for Child in ChildList:
            # we are deleting all childs below this Child
            if len(Child['ResourceModel'].Childs) > 0:
                CurrentKey= Child['ResourceModel'].Key
                dbQuery = Child['ResourceModel'].Table.query
                # Browse all childs
                dbQuery = dbQuery.filter(getattr(Child['ResourceModel'].Table, Child['ParentKey']) == ParentKeyValue)
                AllChildElements = dbQuery.all()
                # Delete all "subchild" for each child
                for Element in AllChildElements:
                    CurrentKeyValue = getattr(Element, CurrentKey)
                    self.delete_all_childs(Child['ResourceModel'].Childs, CurrentKeyValue)

            # we are deleting all childs records
            dbQuery = Child['ResourceModel'].Table.query
            dbQuery = dbQuery.filter(getattr(Child['ResourceModel'].Table, Child['ParentKey']) == ParentKeyValue)
            AllChildElements = dbQuery.all()
            for Element in AllChildElements:
                db.session.delete(Element)


    def get(self, **kwargs):
        """ display a single element.
        self.Key is the element key provided into the api URL.
        self.ParentKey (optional) : is the foreign key of parent node provided into the api URL
        """
        Key = kwargs[self.Key]
        # Parent or Child Ressource
        OneElement = self.dbTable.query.get_or_404(Key)

        if self.has_parent:
        # we are checking parent key consistency between REST request and Database
        # if not consistent, requested child does not belong to given parents in REST request
            for Parent in self.Parents:
                ParentKey = Parent['ParentKey']
                # ParentKey value is seek into the received method parameters
                ParentKeyValue = kwargs.get(ParentKey)
                ParentNode = Parent['ResourceModel'].Table.query.get_or_404(ParentKeyValue)
                if getattr(OneElement, ParentKey) != ParentKeyValue:
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
        # we are checking parent key consistency between REST request and Database
        # if not consistent, requested child does not belong to given parents in REST request
            for Parent in self.Parents:
                ParentKey = Parent['ParentKey']
                # ParentKey value is seek into the received method parameters
                ParentKeyValue = kwargs.get(ParentKey)
                ParentNode = Parent['ResourceModel'].Table.query.get_or_404(ParentKeyValue)
                if getattr(OneElement, ParentKey) != ParentKeyValue:
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
            # we are deleting all childs below parent
            ParentKeyValue = kwargs.get(self.Key)
            self.delete_all_childs(self.Childs, ParentKeyValue)

        # Delete a Parent or a Child resource
        Key = kwargs[self.Key]
        OneElement = self.dbTable.query.get_or_404(Key)

        if self.has_parent:
        # we are checking parent key consistency between REST request and Database
        # if not consistent, requested child does not belong to given parents in REST request
            for Parent in self.Parents:
                ParentKey = Parent['ParentKey']
                # ParentKey value is seek into the received method parameters
                ParentKeyValue = kwargs.get(ParentKey)
                ParentNode = Parent['ResourceModel'].Table.query.get_or_404(ParentKeyValue)
                if getattr(OneElement, ParentKey) != ParentKeyValue:
                    abort(404)

        db.session.delete(OneElement)
        db.session.commit()
        return jsonify({'result': True})