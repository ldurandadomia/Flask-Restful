from restapp import app
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from flask import url_for
from restapp import db, models


def make_public_switch(switch):
    """affiche les attributs du switch en remplacant l'ID par son URI"""
    new_switch = {}
    for field in switch:
        if field == 'Id':
            new_switch['uri'] = url_for('get_switch', switch_id=switch['Id'], _external=True)
        else:
            new_switch[field] = switch[field]
    return new_switch


def make_public_port(port):
    """affiche les attributs du port en remplacant l'ID par son URI"""
    new_port = {}
    for field in port:
        if field == 'port_id':
            new_port['uri'] = url_for('get_port', switch_id=port['switch_id'], port_id=port['port_id'], _external=True)
        else:
            new_port[field] = port[field]
    return new_port


#############################
# REPONSES AUX METHODES GET #
#############################


@app.route('/todo/api/v1.0/Switches', methods=['GET'])
def get_switches():
    """affiche tous les switchs de l'infrastructure ainsi que leurs ports"""
    AllSwitches = []
    try:
        dbSwitches = models.Switches.query.all()
    except:
        abort(400)
    for dbSwitch in dbSwitches:
        Switch = dbSwitch.GetAllAttributes()
        HasPort = True
        try:
            AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=dbSwitch.Id).all()
        except:
            HasPort = False
        if HasPort:
            Ports = []
            for Port in AllSwitchPorts:
                Ports.append(make_public_port(Port.GetAllAttributes()))
            Switch['Ports'] = Ports
        AllSwitches.append(Switch)
    return jsonify({'Switches': [make_public_switch(Switch) for Switch in AllSwitches]})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>', methods=['GET'])
def get_switch(switch_id):
    """affiche un switch de l'infrastructure ainsi que ses ports"""
    try:
        Switch = models.Switches.query.get(switch_id).GetAllAttributes()
    except:
        abort(404)
    HasPort = True
    try:
        AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=switch_id).all()
    except:
        HasPort = False
    Ports = []
    for Port in AllSwitchPorts:
        Ports.append(make_public_port(Port.GetAllAttributes()))
    if HasPort:
        Switch['Ports'] = Ports
    return jsonify({'Switch': make_public_switch(Switch)})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports', methods=['GET'])
def get_ports(switch_id):
    """affiche tous les ports d'un switch de l'infrastructure"""
    try:
        AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=switch_id).all()
    except:
        abort(404)
    Ports = []
    for Port in AllSwitchPorts:
        Ports.append(make_public_port(Port.GetAllAttributes()))
    return jsonify({'Ports': Ports})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports/<int:port_id>', methods=['GET'])
def get_port(switch_id, port_id):
    """affiche un port d'un switch de l'infrastructure"""
    try:
        Port = models.Ports.query.get(port_id)
    except:
        abort(404)
    if Port.Switch_Id != switch_id:
        abort(404)
    return jsonify({'Port': make_public_port(Port.GetAllAttributes())})


##############################
# REPONSES AUX METHODES POST #
##############################


@app.route('/todo/api/v1.0/Switches', methods=['POST'])
def create_switch():
    """ajoute un port a un switch de l'infrastructure"""
    if not request.json or not 'ManagementIP' in request.json:
        abort(400)
    Switch = {
        'ManagementIP': request.json['ManagementIP'],
        'Name': request.json.get('Name', 'no name')
    }
    try:
        un_switch = models.Switches(Name=Switch['Name'], ManagementIP=Switch['ManagementIP'])
        db.session.add(un_switch)
        db.session.commit()
    except:
        abort(400)
    return jsonify({'switch': make_public_switch(un_switch.GetAllAttributes())}), 201


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports', methods=['POST'])
def create_port(switch_id):
    """ajoute un port a un switch de l'infrastructure"""
    if not request.json or not 'Name' in request.json:
        abort(400)
    try:
        un_switch = models.Switches.query.get(switch_id)
    except:
        abort(404)
    try:
        un_port = models.Ports(Name=request.json['Name'],
                               Speed=request.json.get('Speed', "1000"),
                               Duplex=request.json.get('Duplex', "full"),
                               Status=request.json.get('Status', "disable"),
                               SwitchNode=un_switch)
        db.session.add(un_port)
        db.session.commit()
    except:
        abort(404)
    return jsonify({'port': make_public_port(un_port.GetAllAttributes())}), 201


#############################
# REPONSES AUX METHODES PUT #
#############################


@app.route('/todo/api/v1.0/Switches/<int:switch_id>', methods=['PUT'])
def update_switch(switch_id):
    """modifie un switch de l'infrastructure"""
    try:
        Switch = models.Switches.query.get(switch_id)
        if Switch.Id != switch_id:
            abort(404)
    except:
        abort(404)
    if not request.json:
        abort(400)
    if 'Name' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'ManagementIP' in request.json and type(request.json['ManagementIP']) is not unicode:
        abort(400)
    Switch.Name = request.json.get('Name', Switch.Name)
    Switch.ManagementIP = request.json.get('ManagementIP', Switch.ManagementIP)
    try:
        db.session.commit()
    except:
        abort(400)
    return jsonify({'switch': make_public_switch(Switch.GetAllAttributes())})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports/<int:port_id>', methods=['PUT'])
def update_port(switch_id, port_id):
    """modifie le port d'un switch de l'infrastructure"""
    try:
        Port = models.Ports.query.get(port_id)
        if Port.Switch_Id != switch_id:
            abort(404)
    except:
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
    Port.Name = request.json.get('Name', Port.Name)
    Port.Speed = request.json.get('Speed', Port.Speed)
    Port.Duplex = request.json.get('Duplex', Port.Duplex)
    Port.Status = request.json.get('Status', Port.Status)
    db.session.commit()
    return jsonify({'port': make_public_port(Port.GetAllAttributes())})


################################
# REPONSES AUX METHODES DELETE #
################################


@app.route('/todo/api/v1.0/Switches/<int:switch_id>', methods=['DELETE'])
def delete_switch(switch_id):
    """supprime un switch de l'infrastructure ainsi que ses ports"""
    try:
        AllSwitchPorts = models.Ports.query.filter_by(SwitchId=switch_id).all()
        for port in AllSwitchPorts:
            db.session.delete(port)
    except:
        pass
    try:
        Switch = models.Switches.query.get(switch_id)
        db.session.delete(Switch)
        db.session.commit()
    except:
        abort(404)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/Switches/<int:switch_id>/Ports/<int:port_id>', methods=['DELETE'])
def delete_port(switch_id, port_id):
    """supprime le port d'un switch de l'infrastructure"""
    try:
        Port = models.Ports.query.get(port_id)
        if Port.Switch_Id != switch_id:
            abort(404)
        db.session.delete(Port)
        db.session.commit()
    except:
        abort(404)
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
