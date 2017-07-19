from <module> import app
from flask import request
from flask import Response
import requests


@app.route('/inconming/<path:url_path>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def reroute_to_nso(url_path):
    """ reroute to NSO application"""
    new_response = requests.request(
        method=request.method,
        url=request.url.replace(':5000/incoming', ':8080/nso'),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in new_response.raw.headers.items()
               if name.lower() not in excluded_headers]

    app_response = Response(new_response.content, new_response.status_code, headers)
    return app_response