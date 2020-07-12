import os
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTION'
    response.headers['Access-Control-Allow-Headers'] =\
        'Content-Type, Authorization'
    return response


app.after_request(after_request)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


if __name__ == '__main__':
    app.debug = True
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), threaded=True)
