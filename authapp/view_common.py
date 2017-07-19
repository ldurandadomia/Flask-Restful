from flask_restful import fields

author_rule_fields = {
    'Id': fields.Integer,
    'Uuid': fields.Integer,
    'Method': fields.String,
    'Role': fields.String,
    'uri': fields.Url('AuthorizationRule', absolute=True, scheme='http')
}

default_rule_fields = {
    'Id': fields.Integer,
    'Name': fields.String,
    'Method': fields.String,
    'Role': fields.String,
    'uri': fields.Url('DefaultRule', absolute=True, scheme='http')
}

object_fields = {
    'Uuid': fields.Integer,
    'Name': fields.String,
    'Id': fields.Integer,
    'uri': fields.Url('Object', absolute=True, scheme='http'),
    'Rules': fields.List(fields.Nested(author_rule_fields))
}
