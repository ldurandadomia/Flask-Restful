from restapp import api
from restapp.view_RestDataCollection import RestDataCollection
from restapp.view_RestDataElement import RestDataElement
from flask_restful import fields

class RestParentChild:
    """Parent Child REST api datamodel"""
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
        # URL Routing attributes
        self.UrlBase = kwargs['UrlBase']
        self.ParentCollectionName = kwargs['ParentCollectionName']
        self.ChildCollectionName = kwargs['ChildCollectionName']
        self.ParentCollectionEndPoint = kwargs['ParentCollectionEndPoint']
        self.ParentSingleElementEndPoint = kwargs['ParentSingleElementEndPoint']
        self.ChildCollectionEndPoint = kwargs['ChildCollectionEndPoint']
        self.ChildSingleElementEndPoint = kwargs['ChildSingleElementEndPoint']

        # Database
        self.Database = kwargs['Database']

        # Parent Datamodel
        self.ParentTable = kwargs['ParentTable']
        self.ParentKeyName = kwargs['ParentKeyName']
        self.ParentKeyType = kwargs['ParentKeyType']

        # Child Datamodel
        self.ChildTable = kwargs['ChildTable']
        self.ChildKeyName = kwargs['ChildKeyName']
        self.ChildKeyType = kwargs['ChildKeyType']
        self.ParentForeignKeyName = kwargs['ParentForeignKeyName']
        self.ParentBackRefField = kwargs['ParentBackRefField']

        # Parent display format
        self.ParentCollectionTitle = kwargs['ParentCollectionTitle']
        self.ParentSingleElementTitle = kwargs['ParentSingleElementTitle']
        self.ParentDisplayFormat = kwargs['ParentDisplayFormat']
        self.ParentPostParser = kwargs['ParentPostParser']
        self.ParentPutParser = kwargs['ParentPutParser']
        self.ParentDisplayFormat['uri'] = fields.Url(self.ParentSingleElementEndPoint, absolute=True, scheme='http')

        # Child display format
        self.ChildCollectionTitle = kwargs['ChildCollectionTitle']
        self.ChildSingleElementTitle = kwargs['ChildSingleElementTitle']
        self.ChildDisplayFormat = kwargs['ChildDisplayFormat']
        self.ChildPostParser = kwargs['ChildPostParser']
        self.ChildPutParser = kwargs['ChildPutParser']
        self.ChildDisplayFormat['uri'] = fields.Url(self.ChildSingleElementEndPoint, absolute=True, scheme='http')

        # Parent collection route instantiation
        ParentCollectionRoute = self.UrlBase + '/' + self.ParentCollectionName
        api.add_resource(RestDataCollection, ParentCollectionRoute,
            endpoint=self.ParentCollectionEndPoint,
            resource_class_kwargs={'Database': self.Database,
                                   'Table': self.ParentTable,
                                   'CollectionTitle': self.ParentCollectionTitle,
                                   'SingleElementTitle': self.ParentSingleElementTitle,
                                   'DisplayFormat': self.ParentDisplayFormat,
                                   'PostParser': self.ParentPostParser})

        # Parent single element route instantiation
        ParentElementRoute = ParentCollectionRoute + '/'
        ParentElementRoute += '<' + self.ParentKeyType + ':' + self.ParentKeyName + '>'
        api.add_resource(RestDataElement, ParentElementRoute,
            endpoint=self.ParentSingleElementEndPoint,
            resource_class_kwargs={'Database': self.Database,
                                   'Table': self.ParentTable,
                                   'ChildTable': self.ChildTable,
                                   'Key': self.ParentKeyName,
                                   'ChildParentKey': self.ParentForeignKeyName,
                                   'SingleElementTitle': self.ParentSingleElementTitle,
                                   'DisplayFormat': self.ParentDisplayFormat,
                                   'PutParser': self.ParentPutParser})

        # Child collection route instantiation
        ChildCollectionRoute = ParentCollectionRoute + '/'
        ChildCollectionRoute += '<' + self.ParentKeyType + ':' + self.ParentForeignKeyName + '>' + '/'
        ChildCollectionRoute += self.ChildCollectionName
        api.add_resource(RestDataCollection, ChildCollectionRoute,
            endpoint=self.ChildCollectionEndPoint,
            resource_class_kwargs={'Database': self.Database,
                                   'Table': self.ChildTable,
                                   'ParentTable': self.ParentTable,
                                   'ParentKey': self.ParentForeignKeyName,
                                   'ParentBackRefField': self.ParentBackRefField,
                                   'CollectionTitle': self.ChildCollectionTitle,
                                   'SingleElementTitle': self.ChildSingleElementTitle,
                                   'DisplayFormat': self.ChildDisplayFormat,
                                   'PostParser': self.ChildPostParser})

        # Child single element route instantiation
        ChildElementRoute = ChildCollectionRoute + '/'
        ChildElementRoute += '<' + self.ChildKeyType + ':' + self.ChildKeyName + '>'
        api.add_resource(RestDataElement, ChildElementRoute,
            endpoint=self.ChildSingleElementEndPoint,
            resource_class_kwargs={'Database': self.Database,
                                   'Table': self.ChildTable,
                                   'Key': self.ChildKeyName,
                                   'ParentKey': self.ParentForeignKeyName,
                                   'SingleElementTitle': self.ChildSingleElementTitle,
                                   'DisplayFormat': self.ChildDisplayFormat,
                                   'PutParser': self.ChildPutParser})
