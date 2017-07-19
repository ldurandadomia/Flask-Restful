from flask_restful import reqparse
from flask_restful import fields
from restapp import api
from restapp import db
from restapp import models
from restapp.view_RestDataCollection_v2 import RestDataCollection
from restapp.view_RestDataElement_v2 import RestDataElement
from restapp.view_RestResourceModel import RestResourceModel


#############################################
# Port Fields parsers for GET, POST and PUT #
#############################################

# Fields to be displayed when issuing a GET on a Port collection
port_fields_v6 = {
    'Name': fields.String,
    'Speed': fields.String,
    'Duplex': fields.String,
    'Status': fields.String,
    'uri': fields.Url('Port_v6', absolute=True, scheme='http')
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
switch_fields_v6 = {
    'ManagementIP': fields.String,
    'Name': fields.String,
    'uri': fields.Url('Switch_v6', absolute=True, scheme='http'),
    'Ports': fields.List(fields.Nested(port_fields_v6))
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


##############################
# REST Resources description #
##############################


SwitchesResourceModel = RestResourceModel(db, models.Switches, 'Id', 'AllSwitches', 'ASwitch',
                                   switch_fields_v6, switch_post_parser, switch_put_parser )

PortsResourceModel = RestResourceModel(db, models.Ports, 'Id', 'AllPorts', 'APort',
                                   port_fields_v6, port_post_parser, port_put_parser )

SwitchesResourceModel.add_a_child( PortsResourceModel, 'Switch_Id', 'SwitchNode')


###############
# API routing #
###############

api.add_resource(RestDataCollection, '/todo/api/v6.0/Switches', endpoint='Switches_v6',
                 resource_class_kwargs={ 'RestResourceModel': SwitchesResourceModel })

api.add_resource(RestDataElement, '/todo/api/v6.0/Switches/<int:Id>', endpoint='Switch_v6',
                 resource_class_kwargs={ 'RestResourceModel': SwitchesResourceModel })

api.add_resource(RestDataCollection, '/todo/api/v6.0/Switches/<int:Switch_Id>/Ports', endpoint='Ports_v6',
                 resource_class_kwargs={ 'RestResourceModel': PortsResourceModel })

api.add_resource(RestDataElement, '/todo/api/v6.0/Switches/<int:Switch_Id>/Ports/<int:Id>', endpoint='Port_v6',
                 resource_class_kwargs={ 'RestResourceModel': PortsResourceModel })
