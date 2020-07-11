from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=True)