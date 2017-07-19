from flask_restful import fields


child_fields = {
    '<Atrribute1>': fields.String,
    '<Atrribute2>': fields.String,
    ...
    '<AtrributeN>': fields.String,
    'uri': fields.Url('child', absolute=True, scheme='http'),
}

parent_fields = {
    '<Atrribute1>': fields.String,
    '<Atrribute2>': fields.String,
    ...
    '<AtrributeN>': fields.String,
    'uri': fields.Url('parent', absolute=True, scheme='http'),
    'childs': fields.List(fields.Nested(child_fields))
}
