
class RestResourceModel(object):
    """ Manage description of a RestResource
    """

    def __init__(self, Database, Table, Key, CollectionTitle, SingleElementTitle, DisplayFormat, PostParser, PutParser ):
        self.Database = Database
        self.Table = Table
        self.Key = Key
        self.CollectionTitle = CollectionTitle
        self.SingleElementTitle = SingleElementTitle
        self.DisplayFormat = DisplayFormat
        self.PostParser = PostParser
        self.PutParser = PutParser
        self.Parents = []
        self.Childs = []

    def add_a_child(self, ChildResourceModel, ChildParentKey, ParentBackRefField ):
        self.Childs.append( {'ParentKey': ChildParentKey,
                             'ParentBackRefField': ParentBackRefField,
                             'ResourceModel': ChildResourceModel})
        ChildResourceModel.Parents.append( {'ParentKey': ChildParentKey,
                             'ParentBackRefField': ParentBackRefField,
                             'ResourceModel': self})
