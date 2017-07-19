from restapp import app
from flask import jsonify
from flask import abort
from flask import request
from restapp import db, models
from view_common_v1 import make_public_port


#############################
# REPONSES AUX METHODES GET #
#############################


@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>/Ports/<int:Port_Id>', methods=['GET'])
def get_port(Switch_Id, Port_Id):
    """affiche un port d'un switch de l'infrastructure"""
    try:
        Port = models.Ports.query.get(Port_Id)
    except:
        abort(404)
    if Port.Switch_Id != Switch_Id:
        abort(404)
    return jsonify({'Port': make_public_port(Port.GetAllAttributes())})


##############################
# REPONSES AUX METHODES POST #
##############################

# Non applicable


#############################
# REPONSES AUX METHODES PUT #
#############################


@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>/Ports/<int:Port_Id>', methods=['PUT'])
def update_port(Switch_Id, Port_Id):
    """modifie le port d'un switch de l'infrastructure"""
    try:
        Port = models.Ports.query.get(Port_Id)
        if Port.Switch_Id != Switch_Id:
            abort(404)
    except:
        abort(404)
    if not request.json:
        abort(400)
    if 'Name' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'Speed' in request.json and type(request.json['Speed']) != unicode:
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


@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>/Ports/<int:Port_Id>', methods=['DELETE'])
def delete_port(Switch_Id, Port_Id):
    """supprime le port d'un switch de l'infrastructure"""
    try:
        Port = models.Ports.query.get(Port_Id)
        if Port.Switch_Id != Switch_Id:
            abort(404)
        db.session.delete(Port)
        db.session.commit()
    except:
        abort(404)
    return jsonify({'result': True})
