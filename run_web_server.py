from flask import Flask
from web.Tasks import tasks_api
from web.Environments import environments_api

app = Flask(__name__)
app.register_blueprint(tasks_api)
app.register_blueprint(environments_api)

if __name__ == "__main__":
    app.run()
