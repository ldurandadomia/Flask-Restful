from flask import Flask
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class SetOfSwitches(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def post(self):
        pass

class SingleSwitch(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def post(self):
        pass

class SetOfPorts(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def post(self):
        pass

class SinglePort(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def post(self):
        pass

api.add_resource(SetOfSwitches, '/todo/api/v2.0/Switches', endpoint = 'Switches')
api.add_resource(SingleSwitch, '/todo/api/v2.0/Switches/<int:switch_id>', endpoint = 'Switch')
api.add_resource(SetOfPorts, '/todo/api/v2.0/Switches/<int:switch_id>/Ports', endpoint = 'Ports')
api.add_resource(SinglePort, '/todo/api/v2.0/Switches/<int:switch_id>/Ports/<int:port_id>', endpoint = 'Port')