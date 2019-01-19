from flask import Flask
from web.Tasks import tasks_api
from web.Environments import environments_api
from web.Storage import storage_api
from web.AutoBuild import autobuild_api

app = Flask(__name__)
app.register_blueprint(tasks_api)
app.register_blueprint(environments_api)
app.register_blueprint(storage_api)
app.register_blueprint(autobuild_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
