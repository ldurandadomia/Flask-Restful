from flask_restful import reqparse
from flask_restful import fields
from restapp import api
from restapp import db
from restapp import models
from restapp.view_RestDataCollection import RestDataCollection
from restapp.view_RestDataElement import RestDataElement


#############################################
# Port Fields parsers for GET, POST and PUT #
#############################################

# Fields to be displayed when issuing a GET on a Port collection
port_fields_v4 = {
    'Name': fields.String,
    'Speed': fields.String,
    'Duplex': fields.String,
    'Status': fields.String,
    'uri': fields.Url('Port_v4', absolute=True, scheme='http')
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
switch_fields_v4 = {
    'ManagementIP': fields.String,
    'Name': fields.String,
    'uri': fields.Url('Switch_v4', absolute=True, scheme='http'),
    'Ports': fields.List(fields.Nested(port_fields_v4))
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

api.add_resource(RestDataCollection, '/todo/api/v4.0/Switches', endpoint='Switches_v4',
                 resource_class_kwargs={ 'Database': db,
                                         'Table': models.Switches,
                                         'CollectionTitle': 'AllSwitches',
                                         'SingleElementTitle' : 'ASwitch',
                                         'DisplayFormat' : switch_fields_v4,
                                         'PostParser' : switch_post_parser})

api.add_resource(RestDataElement, '/todo/api/v4.0/Switches/<int:Id>', endpoint='Switch_v4',
                 resource_class_kwargs={ 'Database': db,
                                        'Table': models.Switches,
                                        'ChildTable': models.Ports,
                                        'Key' : 'Id',
                                        'ChildParentKey': 'Switch_Id',
                                        'SingleElementTitle' : 'ASwitch',
                                        'DisplayFormat' : switch_fields_v4,
                                        'PutParser' : switch_put_parser})


api.add_resource(RestDataCollection, '/todo/api/v4.0/Switches/<int:Switch_Id>/Ports', endpoint='Ports_v4',
                 resource_class_kwargs = {'Database': db,
                                         'Table': models.Ports,
                                         'ParentTable': models.Switches,
                                         'ParentKey': 'Switch_Id',
                                         'ParentBackRefField' : 'SwitchNode',
                                         'CollectionTitle': 'AllPorts',
                                         'SingleElementTitle': 'APort',
                                         'DisplayFormat': port_fields_v4,
                                         'PostParser': port_post_parser})

api.add_resource(RestDataElement, '/todo/api/v4.0/Switches/<int:Switch_Id>/Ports/<int:Id>', endpoint='Port_v4',
                 resource_class_kwargs={'Database': db,
                                        'Table': models.Ports,
                                        'Key': 'Id',
                                        'ParentKey': 'Switch_Id',
                                        'SingleElementTitle': 'APort',
                                        'DisplayFormat': port_fields_v4,
                                        'PutParser': port_put_parser})