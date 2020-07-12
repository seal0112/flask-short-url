from . import short_url

@short_url.errorhandler(404)
def pageNotfound(error):
    return make_response(json.dumps('404 not found'), 404)


@short_url.errorhandler(500)
def internalServerError(error):
    logging.error('Server Error: %s', (error))
    return make_response(json.dumps('500 server error'), 500)