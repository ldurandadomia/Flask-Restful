from restapp import api
from restapp.view_RestDataCollection_v3 import RestDataCollection
from restapp.view_RestDataElement_v3 import RestDataElement
from flask_restful import fields

class RestResourceModel(object):
    """ Manage description of a RestResource
    """

    def __init__(self, RouteDescription, Database, Table, Key, GetParser, PostParser, PutParser, NetworkManager):
        self.Database = Database
        self.Table = Table
        self.Key = Key
        self.CollectionTitle = GetParser['CollectionTitle']
        self.SingleElementTitle = GetParser['SingleElementTitle']
        self.DisplayFormat = GetParser['DisplayFields']
        self.PostParser = PostParser
        self.PutParser = PutParser
        self.RouteDescription = RouteDescription
        self.Parents = []
        self.Childs = []
        self.NetworkManager = NetworkManager

    def add_a_child(self, ChildResourceModel, ChildParentKey, ParentBackRefField):
        """add a child REST resource to the current REST resource"""
        self.Childs.append( {'ParentKey': ChildParentKey,
                             'ParentBackRefField': ParentBackRefField,
                             'ResourceModel': ChildResourceModel})
        ChildResourceModel.Parents.append( {'ParentKey': ChildParentKey,
                             'ParentBackRefField': ParentBackRefField,
                             'ResourceModel': self})

    def route_activation(self):
        # add an URI fields to every resource display format
        self.DisplayFormat['uri'] = fields.Url(self.RouteDescription['SingleElementEndPoint'], absolute=True, scheme='http')

        # Collection route instantiation
        Path = '/'
        Parents = self.Parents
        while len(Parents) > 0:
            Path += Parents[0]['ResourceModel'].RouteDescription['ResourceName'] + '/<' \
                  + Parents[0]['ResourceModel'].RouteDescription['KeyType'] + ':' + Parents[0]['ParentKey'] + '>/'
            Parents = Parents[0]['ResourceModel'].Parents

        CollectionRoute = self.RouteDescription['UrlBase'] + Path + self.RouteDescription['ResourceName']
        api.add_resource(RestDataCollection, CollectionRoute,
            endpoint=self.RouteDescription['CollectionEndPoint'],
                         resource_class_kwargs={'RestResourceModel': self})

        # Parent single element route instantiation
        ElementRoute = CollectionRoute + '/'
        ElementRoute += '<' + self.RouteDescription['KeyType'] + ':' + self.Key + '>'
        api.add_resource(RestDataElement, ElementRoute,
            endpoint=self.RouteDescription['SingleElementEndPoint'],
                         resource_class_kwargs={'RestResourceModel': self})