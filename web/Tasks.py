from flask import Blueprint, jsonify, request

from orchestrator.Orchestrator import default_orchestrator
from orchestrator.EnvironmentCreationTask import EnvironmentCreationTask
from orchestrator.PhoenicisWinePackageCreationTask import PhoenicisWinePackageCreationTask
from core.EnvironmentManager import EnvironmentManager

tasks_api = Blueprint('tasks_api', __name__)
environmentManager = EnvironmentManager()

@tasks_api.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == 'POST':
        request_content = request.json
        type = request_content["type"]

        if(type == 'EnvironmentCreationTask'):
            argument = request_content["argument"]
            environment = environmentManager.get_instance(argument)
            environment_creation_task = EnvironmentCreationTask(environment)
            default_orchestrator.run_task(environment_creation_task)

        if(type == 'PhoenicisWinePackageCreationTask'):
            argument = request_content["argument"]
            wine_package_creation_task = PhoenicisWinePackageCreationTask(argument["distribution"], argument["os"], argument["version"], argument["arch"])
            default_orchestrator.run_task(wine_package_creation_task)

        return jsonify(request_content)
    else:
        return jsonify(default_orchestrator.tasks())
