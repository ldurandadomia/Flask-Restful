from restapp import app
from flask import jsonify
from flask import abort
from flask import request
from restapp import db, models
from view_common_v1 import make_public_port


#############################
# REPONSES AUX METHODES GET #
#############################

@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>/Ports', methods=['GET'])
def get_ports(Switch_Id):
    """affiche tous les ports d'un switch de l'infrastructure"""
    try:
        AllSwitchPorts = models.Ports.query.filter_by(Switch_Id=Switch_Id).all()
    except:
        abort(404)
    Ports = []
    for Port in AllSwitchPorts:
        Ports.append(make_public_port(Port.GetAllAttributes()))
    return jsonify({'Ports': Ports})


##############################
# REPONSES AUX METHODES POST #
##############################

@app.route('/todo/api/v1.0/Switches/<int:Switch_Id>/Ports', methods=['POST'])
def create_port(Switch_Id):
    """ajoute un port a un switch de l'infrastructure"""
    if not request.json or not 'Name' in request.json:
        abort(400)
    try:
        un_switch = models.Switches.query.get(Switch_Id)
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
        abort(400)
    return jsonify({'port': make_public_port(un_port.GetAllAttributes())}), 201

#############################
# REPONSES AUX METHODES PUT #
#############################

# Non applicable


################################
# REPONSES AUX METHODES DELETE #
################################

# Non applicable
