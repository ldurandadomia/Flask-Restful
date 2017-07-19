from flask import abort, request
from flask_restful import Resource, marshal


class RestDataCollection(Resource):
    """ RestDataCollection:
    Manage with REST a collection of elements :
        - POST : is allowing to add an element to the collection
        - GET : is allowing to display all elements of the collection
    """

    def __init__(self, **kwargs):
        """ RestDataCollection constructor:
        - Database : SQL database which is containing table
        - Table : data persistence table
        - Collection Title : JSON title to display for the whole collection display
        - SingleElementTitle : JSON title to display for a single element display
        - DisplayFormat : JSON list of fields to be displayed when a GET is issued
        - PostParser : JSON list of fields to be parsed when a POST is received
        - ParentKey (optional) : ParentKey name in Child object model
        - ParentBackRefField (optional) : Virtual field used in Child object to reference Parent object
        - ParentTable (optional) : parent object data persistence table
        """
        super(RestDataCollection, self).__init__()
        self.Database = kwargs['Database']
        self.dbTable = kwargs['Table']
        self.CollectionTitle = kwargs['CollectionTitle']
        self.SingleElementTitle = kwargs['SingleElementTitle']
        self.DisplayFormat = kwargs['DisplayFormat']
        self.PostParser = kwargs['PostParser']

        self.has_parent = False
        if kwargs.has_key('ParentKey'):
            self.has_parent = True
            self.ParentKey = kwargs['ParentKey']
            self.ParentBackRefField = kwargs['ParentBackRefField']
            self.dbParentTable = kwargs['ParentTable']


    def get(self,**kwargs):
        """display all RestDataCollection elements
        result filtering using "?" operator at the end of REST URL is supported"""
        # Manage GET query filtering
        Filter_Attributes = request.args
        dbQuery = self.dbTable.query

        Filter_Params = dict()
        for attribute in Filter_Attributes:
            if self.DisplayFormat.has_key(attribute):
                Filter_Params[attribute] = Filter_Attributes[attribute]

        try:
            # Manage query filter
            for ParamName, ParamValue in Filter_Params.items():
                dbQuery = dbQuery.filter(getattr(self.dbTable, ParamName) == ParamValue)
            if self.has_parent:
            # Child Ressources additional filter on provided parent key
                    ParentKeyValue = kwargs.get(self.ParentKey)
                    dbQuery = dbQuery.filter(getattr(self.dbTable, self.ParentKey) == ParentKeyValue)
            # Parent or Child query
            dbEntries = dbQuery.all()
        except:
            abort(400)

        if dbEntries == None:
            abort(404)
        return marshal(dbEntries, self.DisplayFormat, self.CollectionTitle), 200


    def post(self, **kwargs):
        """add a new element to the RestDataCollection"""
        args = self.PostParser.parse_args()
        argdict = dict(args)
        try:
            # Parent Ressource
            OneElement = self.dbTable()
            for attribut in argdict.keys():
                setattr(OneElement, attribut, getattr(args, attribut))

            # Child Ressource
            if self.has_parent:
                ParentKeyValue = kwargs.get(self.ParentKey)
                ParentNode = self.dbParentTable.query.get_or_404(ParentKeyValue)
                setattr(OneElement, self.ParentBackRefField, ParentNode)
            self.Database.session.add(OneElement)
            self.Database.session.commit()
        except:
            abort(400)
        return marshal(OneElement, self.DisplayFormat, self.SingleElementTitle), 201