from flask_restful import fields


port_fields = {
    'Name': fields.String,
    'Speed': fields.String,
    'Duplex': fields.String,
    'Status': fields.String,
    'uri': fields.Url('Port', absolute=True, scheme='http'),
}

switch_fields = {
    'ManagementIP': fields.String,
    'Name': fields.String,
    'uri': fields.Url('Switch_v3', absolute=True, scheme='http'),
    'Ports': fields.List(fields.Nested(port_fields))
}
