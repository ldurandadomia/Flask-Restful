from flask import url_for


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
        if field == 'Port_Id':
            # Les parametres de la fonction url_for sont :
            #     le nom de la methode (ici get_port)
            #     et les parametres passes dans l'URL (definit dans app.route)
            new_port['uri'] = url_for('get_port', Switch_Id=port['Switch_Id'], Port_Id=port['Port_Id'], _external=True)
        else:
            new_port[field] = port[field]
    return new_port
