from restapp import app
from flask import jsonify
from flask import abort
from flask import request
from restapp import db, models
from view_common_v1 import make_public_port, make_public_switch


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



##############################
# REPONSES AUX METHODES POST #
##############################


@app.route('/todo/api/v1.0/Switches', methods=['POST'])
def create_switch():
    """ajoute un switch a l'infrastructure"""
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



#############################
# REPONSES AUX METHODES PUT #
#############################

# Non applicable



################################
# REPONSES AUX METHODES DELETE #
################################

# Non applicable