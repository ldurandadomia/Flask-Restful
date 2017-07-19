from restapp import app
from flask import jsonify
from flask import abort
from flask import request
from restapp import db, models
from view_common_v1 import make_public_port, make_public_switch


#############################
# REPONSES AUX METHODES GET #
#############################


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


##############################
# REPONSES AUX METHODES POST #
##############################

# Non applicable


#############################
# REPONSES AUX METHODES PUT #
#############################


@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>', methods=['PUT'])
def update_switch(Switch_Id):
    """modifie un switch de l'infrastructure"""
    try:
        Switch = models.Switches.query.get(Switch_Id)
        if Switch.Id != Switch_Id:
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


################################
# REPONSES AUX METHODES DELETE #
################################


@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>', methods=['DELETE'])
def delete_switch(Switch_Id):
    """supprime un switch de l'infrastructure ainsi que ses ports"""
    try:
        AllSwitchPorts = models.Ports.query.filter_by(SwitchId=Switch_Id).all()
        for port in AllSwitchPorts:
            db.session.delete(port)
    except:
        pass
    try:
        Switch = models.Switches.query.get(Switch_Id)
        db.session.delete(Switch)
        db.session.commit()
    except:
        abort(404)
    return jsonify({'result': True})
