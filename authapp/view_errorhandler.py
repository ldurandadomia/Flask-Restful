from flask_restful import Api


class MyApi(Api):
    def handle_error(self, e):
        """ Overrides the handle_error() method of the Api and adds custom error handling
        :param e: error object
        """
        code = getattr(e, 'code', 500)  # Gets code or defaults to 500
        if code == 404:
            return self.make_response({
                'message': 'not-found',
                'code': 404
            }, 404)
        return super(MyApi, self).handle_error(e)  # handle others the default way