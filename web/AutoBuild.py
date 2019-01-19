from flask import Blueprint, jsonify

from core.ConfigurationReader import ConfigurationReader
from storage.PackageStore import PackageStore
from orchestrator.Orchestrator import default_orchestrator
from orchestrator.PhoenicisWinePackageCreationTask import PhoenicisWinePackageCreationTask

autobuild_api = Blueprint('autobuild_api', __name__)
packageStore = PackageStore()

@autobuild_api.route("/autobuild")
def autobuild():
    autobuild_configuration = ConfigurationReader().read("autobuild")

    for watched in autobuild_configuration["watched"]:
        for distribution in watched["distribution"]:
            for operatingSystem in watched["operatingSystem"]:
                for arch in watched["arch"]:
                    distribution_full_name = "-".join([distribution, operatingSystem, arch])
                    print("Building for %s" % distribution_full_name)
                    for version in packageStore.fetch_missing_versions(distribution_full_name):
                        wine_package_creation_task = PhoenicisWinePackageCreationTask(distribution, operatingSystem, version, arch)
                        default_orchestrator.run_task(wine_package_creation_task)

    return jsonify({"status": "ok"})