#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request
from flask import make_response
from flask import url_for

app = Flask(__name__)
Switches = [
    {
        'id': 1,
        'ManagementIP': u'192.168.1.1',
        'Name': u'sw1.tst.fr',
        'Ports': [
            {
                'id': 1,
                'Name': u'Ethernet0/1',
                'Speed': u'1000',
                'Duplex': u'full',
                'Status': u'enable'
            },
            {
                'id': 2,
                'Name': u'Ethernet0/2',
                'Speed': u'1000',
                'Duplex': u'full',
                'Status': u'disable'
            }
        ]
    },
    {
        'id': 2,
        'ManagementIP': u'192.168.1.2',
        'Name': u'sw2.tst.fr',
        'Ports': [
            {
                'id': 1,
                'Name': u'Ethernet2/1',
                'Speed': u'1000',
                'Duplex': u'full',
                'Status': u'disable'
            },
            {
                'id': 2,
                'Name': u'Ethernet2/2',
                'Speed': u'1000',
                'Duplex': u'full',
                'Status': u'enable'
            }
        ]
    }
]


def make_public_switch(switch):
    """affiche les attributs du switch en remplacant l'ID par son URI"""
    new_switch = {}
    for field in switch:
        if field == 'id':
            new_switch['uri'] = url_for('get_switch', switch_id=switch['id'], _external=True)
        else:
            new_switch[field] = switch[field]
    return new_switch


#############################
# REPONSES AUX METHODES GET #
#############################


@app.route('/todo/api/v1.0/Switches', methods=['GET'])
def get_switches():
    """affiche tous les switchs de l'infrastructure"""
    return jsonify({'Switches': [make_public_switch(Switch) for Switch in Switches]})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>', methods=['GET'])
def get_switch(switch_id):
    """affiche un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    return jsonify({'Switch': Switch[0]})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports', methods=['GET'])
def get_ports(switch_id):
    """affiche tous les ports d'un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    return jsonify({'Ports': Switch[0]['Ports']})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports/<int:port_id>', methods=['GET'])
def get_port(switch_id, port_id):
    """affiche un port d'un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    Port = [Port for Port in Switch[0]['Ports'] if Port['id'] == port_id]
    if len(Port) == 0:
        abort(404)
    return jsonify({'Port': Port[0]})


##############################
# REPONSES AUX METHODES POST #
##############################


@app.route('/todo/api/v1.0/Switches', methods=['POST'])
def create_switch():
    """ajoute un switch a l'infrastructure"""
    if not request.json or not 'ManagementIP' in request.json:
        abort(400)
    Switch = {
        'id': Switches[-1]['id'] + 1,
        'ManagementIP': request.json['ManagementIP'],
        'Name': request.json.get('Name', "sw_{}".format(str(Switches[-1]['id'] + 1)))
    }
    Switches.append(Switch)
    return jsonify({'switch': Switch}), 201


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports', methods=['POST'])
def create_port(switch_id):
    """ajoute un port a un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    if not request.json or not 'Name' in request.json:
        abort(400)

    Port = {
        'id': Switch[0]['Ports'][-1]['id'] + 1,
        'Name': request.json['Name'],
        'Speed': request.json.get('Speed', "1000"),
        'Duplex': request.json.get('Duplex', "full"),
        'status': request.json.get('Status', "disable")
    }
    Switch[0]['Ports'].append(Port)
    return jsonify({'port': Port}), 201


#############################
# REPONSES AUX METHODES PUT #
#############################


@app.route('/todo/api/v1.0/Switches/<int:switch_id>', methods=['PUT'])
def update_switch(switch_id):
    """modifie un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Name' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'ManagementIP' in request.json and type(request.json['ManagementIP']) is not unicode:
        abort(400)
    Switch[0]['Name'] = request.json.get('Name', Switch[0]['Name'])
    Switch[0]['ManagementIP'] = request.json.get('ManagementIP', Switch[0]['ManagementIP'])
    return jsonify({'switch': Switch[0]})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports/<int:port_id>', methods=['PUT'])
def update_port(switch_id, port_id):
    """modifie le port d'un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    Port = [Port for Port in Switch[0]['Ports'] if Port['id'] == port_id]
    if len(Port) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Name' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'Speed' in request.json and type(request.json['Status']) != unicode:
        abort(400)
    if 'Duplex' in request.json and type(request.json['Duplex']) != unicode:
        abort(400)
    if 'Status' in request.json and type(request.json['Status']) != unicode:
        abort(400)
    Port[0]['Name'] = request.json.get('Name', Port[0]['Name'])
    Port[0]['Speed'] = request.json.get('Speed', Port[0]['Speed'])
    Port[0]['Duplex'] = request.json.get('Duplex', Port[0]['Duplex'])
    Port[0]['Status'] = request.json.get('Status', Port[0]['Status'])
    return jsonify({'port': Port[0]})


################################
# REPONSES AUX METHODES DELETE #
################################


@app.route('/todo/api/v1.0/Switches/<int:switch_id>', methods=['DELETE'])
def delete_switch(switch_id):
    """supprime un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    Switches.remove(Switch[0])
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports/<int:port_id>', methods=['DELETE'])
def delete_port(switch_id, port_id):
    """supprime le port d'un switch de l'infrastructure"""
    Switch = [Switch for Switch in Switches if Switch['id'] == switch_id]
    if len(Switch) == 0:
        abort(404)
    Port = [Port for Port in Switch[0]['Ports'] if Port['id'] == port_id]
    if len(Port) == 0:
        abort(404)
    Switch[0]['Ports'].remove(Port[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
