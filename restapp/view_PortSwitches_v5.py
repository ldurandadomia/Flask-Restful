from flask_restful import reqparse
from flask_restful import fields
from restapp import db
from restapp import models
from restapp.view_RestParentChild import RestParentChild


#############################################
# Port Fields parsers for GET, POST and PUT #
#############################################

# Fields to be displayed when issuing a GET on a Port collection
port_fields_v5 = {
    'Name': fields.String,
    'Speed': fields.String,
    'Duplex': fields.String,
    'Status': fields.String,
}


# Parser for POST body data when creating a port
port_post_parser = reqparse.RequestParser()
port_post_parser.add_argument('Name', type=str, required=True,
                              help='No port name provided', location='json')
port_post_parser.add_argument('Speed', type=str, default="1000", location='json')
port_post_parser.add_argument('Duplex', type=str, default="full", location='json')
port_post_parser.add_argument('Status', type=str, default="disable", location='json')


# Parser for PUT body data when updating a port
port_put_parser = reqparse.RequestParser()
port_put_parser.add_argument('Name', type=str)
port_put_parser.add_argument('Speed', type=str)
port_put_parser.add_argument('Duplex', type=str)
port_put_parser.add_argument('Status', type=str)



###############################################
# Switch Fields parsers for GET, POST and PUT #
###############################################

# Fields to be displayed when issuing a GET on a Switches collection
switch_fields_v5 = {
    'ManagementIP': fields.String,
    'Name': fields.String,
    'Ports': fields.List(fields.Nested(port_fields_v5))
}


# Parser for POST body data when creating a switch
switch_post_parser = reqparse.RequestParser()
switch_post_parser.add_argument('ManagementIP', type=str, required=True,
                         help='No Management IP address provided', location='json')
switch_post_parser.add_argument('Name', type=str, default="no name", location='json')


# Parser for PUT body data when updating a switch
switch_put_parser = reqparse.RequestParser()
switch_put_parser.add_argument('ManagementIP', type=str, location='json')
switch_put_parser.add_argument('Name', type=str, location='json')


###############
# API routing #
###############

PortSwitchAPI = RestParentChild(
        # URL Routing attributes
        UrlBase = '/todo/api/v5.0',
        ParentCollectionName = 'Switches',
        ChildCollectionName = 'Ports',
        ParentCollectionEndPoint = 'Switches_v5',
        ParentSingleElementEndPoint = 'Switch_v5',
        ChildCollectionEndPoint = 'Ports_v5',
        ChildSingleElementEndPoint = 'Port_v5',

        # Database
        Database = db,

        # Parent Datamodel
        ParentTable = models.Switches,
        ParentKeyName = 'Id',
        ParentKeyType = 'int',

        # Child Datamodel
        ChildTable = models.Ports,
        ChildKeyName = 'Id',
        ChildKeyType = 'int',
        ParentForeignKeyName = 'Switch_Id',
        ParentBackRefField = 'SwitchNode',

        # Parent display format
        ParentCollectionTitle = 'AllSwitches',
        ParentSingleElementTitle = 'ASwitch',
        ParentDisplayFormat = switch_fields_v5,
        ParentPostParser = switch_post_parser,
        ParentPutParser = switch_put_parser,

        # Child display format
        ChildCollectionTitle = 'AllPorts',
        ChildSingleElementTitle = 'APort',
        ChildDisplayFormat = port_fields_v5,
        ChildPostParser = port_post_parser,
        ChildPutParser = port_put_parser
        )