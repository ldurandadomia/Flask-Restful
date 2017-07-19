
class NetworkManager(object):
    """ NetworkManager:
    Manage configuration and operational status information of network nodes :
        - CREATE : Add a new configuration of a network node (initialisation)
        - READ : Query the configuration or operational status of a network node
        - UPDATE : Change the configuration of a network node
        - DELETE : Remove some piece of configuration on a network node (dismantling)
    """

    def __init__(self, ParentsDict):
        """ NetworkManager constructor:
        - Parents : dictionary of all parents resources
        """
        self.Parents = ParentsDict


    def create(self, Element):
        """ add a new piece of configuration (initialisation)"""
        # Nothing to do for the moment ...
        return False


    def read(self, **kwargs):
        """ read the real configuration if needed """
        # Nothing to do for the moment ...
        return True


    def update(self, **kwargs):
        """ change a piece of configuration (update of an existing config)"""
        # Nothing to do for the moment ...
        return False


    def delete(self, **kwargs):
        """ remove a piece of configuration (desactivation of an existing configuration)"""
        # Nothing to do for the moment ...
        return False
