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
        - RestResourceModel : REST Resource description (data model, display format, put and post parser)
        """
        super(RestDataCollection, self).__init__()
        self.ResourceModel = kwargs['RestResourceModel']

        # Parent Object Table Description
        self.Database = self.ResourceModel.Database
        self.dbTable = self.ResourceModel.Table
        self.CollectionTitle = self.ResourceModel.CollectionTitle
        self.SingleElementTitle = self.ResourceModel.SingleElementTitle
        self.DisplayFormat = self.ResourceModel.DisplayFormat
        self.PostParser = self.ResourceModel.PostParser
        self.has_parent = False
        self.NetworkManager = self.ResourceModel.NetworkManager

        self.parents = self.ResourceModel.Parents
        if len(self.parents) > 0:
            self.has_parent = True


    def add_parent_filter(self, Query, ParentList, KeyDict):
        """Manage ParentKey filtering for GET method appied on Childs"""
        for Parent in ParentList:
            ParentKey = Parent['ParentKey']
            # ParentKey value is seek into the received method parameters
            ParentKeyValue = KeyDict.get(ParentKey)
            # Filter is added to NewQuery
            NewQuery = Query.filter(getattr(self.dbTable, ParentKey) == ParentKeyValue)
            GrandParentList = Parent['ResourceModel'].Parents
            if len(GrandParentList) > 0:
                NewQueryGP = self.add_parent_filter(NewQuery, GrandParentList, KeyDict)
                return NewQueryGP
            return NewQuery

    def check_parents(self, ParentList, KeyList, ParentDict):
        """Check if Parent Hierachy is consistent and store Parents Data into ParentDict"""
        for Parent in ParentList:
            ParentKey = Parent['ParentKey']
            # ParentKey value is seek into received method POST parameters (KeyList)
            ParentKeyValue = KeyList.get(ParentKey)
            ParentNode = Parent['ResourceModel'].Table.query.get_or_404(ParentKeyValue)
            Key = Parent['ResourceModel'].RouteDescription['ResourceName']
            ParentDict[Key] = ParentNode

            GrandParentList = Parent['ResourceModel'].Parents
            if len(GrandParentList) > 0:
                self.check_parents(GrandParentList, KeyList, ParentDict)


    def get(self,**kwargs):
        """display all RestDataCollection elements
        result filtering using "?" operator at the end of REST URL is supported"""

        dbQuery = self.dbTable.query

        # Manage GET query filtering (read provided filtering parameters)
        Filter_Attributes = request.args
        Filter_Params = dict()
        for attribute in Filter_Attributes:
            if self.DisplayFormat.has_key(attribute):
                Filter_Params[attribute] = Filter_Attributes[attribute]

        try:
            # Enforce query filter
            for ParamName, ParamValue in Filter_Params.items():
                dbQuery = dbQuery.filter(getattr(self.dbTable, ParamName) == ParamValue)

            if self.has_parent:
                # Child Ressources additional filters on provided parent key
                dbQuery = self.add_parent_filter(dbQuery, self.parents, kwargs)

            # table query
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
                # Retreive all parents and grandparents
                ParentDict = {}
                self.check_parents(self.parents, kwargs, ParentDict)

                # Manage database Child join relationship with its parents
                for Parent in self.parents:
                    ParentKey = Parent['ParentKey']
                    # ParentKey value is seek into the received method parameters
                    ParentKeyValue = kwargs.get(ParentKey)
                    ParentNode = Parent['ResourceModel'].Table.query.get_or_404(ParentKeyValue)
                    # Manage child join with parents in database
                    setattr(OneElement, Parent['ParentBackRefField'], ParentNode)

            # Perform the network change
            self.Database.session.add(OneElement)
            if self.NetworkManager(ParentDict).create(OneElement):
                self.Database.session.commit()
            else:
                self.Database.session.rollback()
        except:
            abort(400)
        return marshal(OneElement, self.DisplayFormat, self.SingleElementTitle), 201