from flask_restful import reqparse
from flask_restful import fields
from restapp import db
from restapp import models
from restapp.view_RestResourceModel_v2 import RestResourceModel
from restapp.controller_NxOS_PortSwitch import NxOS_PortSwitch

#############################################
# Port Fields parsers for GET, POST and PUT #
#############################################

# Fields to be displayed when issuing a GET on a Port collection
port_get_parser = {
    'CollectionTitle': 'AllPorts',
    'SingleElementTitle': 'APort',
    'DisplayFields': {
        'Name': fields.String,
        'Speed': fields.String,
        'Duplex': fields.String,
        'Status': fields.String
    }
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
switch_get_parser = {
    'CollectionTitle': 'AllSwitches',
    'SingleElementTitle': 'ASwitch',
    'DisplayFields': {
        'ManagementIP': fields.String,
        'Name': fields.String,
        'Ports': fields.List(fields.Nested(port_get_parser['DisplayFields']))
    }
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


###########################
# API routing information #
###########################

SwitchesRouteDescription = {
    'UrlBase': '/todo/api/v7.0',
    'ResourceName': 'Switches',
    'CollectionEndPoint': 'Switches_v7',
    'SingleElementEndPoint': 'Switch_v7',
    'KeyType': 'int'
}

PortsRouteDescription = {
    'UrlBase': '/todo/api/v7.0',
    'ResourceName': 'Ports',
    'CollectionEndPoint': 'Ports_v7',
    'SingleElementEndPoint': 'Port_v7',
    'KeyType': 'int'
}


##############################
# REST Resources description #
##############################


SwitchesResourceModel = RestResourceModel(SwitchesRouteDescription, db, models.Switches, 'Id',
                                   switch_get_parser, switch_post_parser, switch_put_parser, NxOS_PortSwitch)

PortsResourceModel = RestResourceModel(PortsRouteDescription, db, models.Ports, 'Id',
                                   port_get_parser, port_post_parser, port_put_parser, NxOS_PortSwitch)


########################################
# REST Resources hierarchy description #
########################################

SwitchesResourceModel.add_a_child(PortsResourceModel, 'Switch_Id', 'SwitchNode')



#####################################
# REST Resources routing activation #
#####################################

SwitchesResourceModel.route_activation()

PortsResourceModel.route_activation()
