from routeapp import app
from flask import jsonify
from flask import abort
from flask import request
import requests


base_url = '/todo/api/'

object_types = ['Switches', 'Ports']

@app.route( base_url + 'v<float:version>/<string:object_name>/<int:object_id>', methods=['GET', 'PUT', 'DELETE'])
def flat_an_object(version, object_name, object_id):
    if (type(version) != type(float())):
        abort(400)

    if ((type(object_name) != type(str())) and (type(object_name) != type(unicode()))):
        abort(400)

    if (type(object_id) != type(int())):
        abort(400)

    if object_name not in object_types:
        abort (400)

    args = {}
    args['Version'] = version
    args['Object Name'] = object_name
    args['Object Id'] = object_id
    args['Method'] = request.method

#
#
# REQUETE A CORRIGER POUR VERIFIER LES REGLES PROPRE A L'OBJET ET NON CELLES PAR DEFAUT
# FAIRE COMME LA VERIF DANS LA METHODE flat_all_objects MAIS AVEC UN PARAMETRE SUPPLEMENTAIRE
# POUR CE FAIRE AJOUTER UN FILTRE EN OPTION DANS LA METHODE GET de view_auth_rules
#
    new_response = requests.request(
        method='GET',
        url='http://127.0.0.1:7000/todo/aaa/v1.0/DefaultRules',
        json={'Name': args['Object Name'], 'Method': args['Method']})

    if new_response.ok == False:
        args['Allowed'] = False
    else:
        args['Allowed'] = True

    return jsonify({'result': args})



@app.route( base_url + 'v<float:version>/<string:object_name>', methods=['GET', 'POST'])
def flat_all_objects(version, object_name):
    if (type(version) != type(float())):
        abort(400)

    if ((type(object_name) != type(str())) and (type(object_name) != type(unicode()))):
        abort(400)

    if object_name not in object_types:
        abort (400)

    args = {}
    args['Version'] = version
    args['Object Name'] = object_name
    args['Method'] = request.method

    new_response = requests.request(
        method='GET',
        url='http://127.0.0.1:7000/todo/aaa/v1.0/DefaultRules',
        json={'Name': args['Object Name'], 'Method': args['Method']})

    if new_response.ok == False:
        args['Allowed'] = False
    else:
        args['Allowed'] = True

    return jsonify({'result': args})



@app.route( base_url + 'v<float:version>/<string:parent_name>/<int:parent_id>/<string:object_name>/<int:object_id>', methods=['GET', 'PUT', 'DELETE'])
def child_an_object(version, parent_name, parent_id, object_name, object_id):
    return jsonify({'result': 'OK'})

@app.route( base_url + 'v<float:version>/<string:parent_name>/<int:parent_id>/<string:object_name>', methods=['GET', 'POST'])
def child_all_objects(version, parent_name, parent_id, object_name):
    return jsonify({'result': 'OK'})