from restapp import app
from flask import request
from flask import Response
import requests

###############################################
# REROUTE DES APPELS VERS L'APPLICATION GOTO  #
###############################################

@app.route('/todo/api/v1.0/goto/<path:url_path>', methods=['GET'])
def reroute_goto(url_path):
    """ reroute to goto application"""
    response=requests.get('http://127.0.0.1:8000/todo/api/v1.0/' + url_path)
    return response.content


@app.route('/todo/api/v1.0/goto2/<path:url_path>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def reroute_goto2(url_path):
    """ reroute to goto2 application"""
    new_response = requests.request(
        method=request.method,
        url=request.url.replace(':5000/todo/api/v1.0/goto2', ':8000/todo/api/v1.0'),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in new_response.raw.headers.items()
               if name.lower() not in excluded_headers]

    app_response = Response(new_response.content, new_response.status_code, headers)
    return app_response