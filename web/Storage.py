from flask import Blueprint, jsonify, send_file

from storage.PackageStore import PackageStore
from orchestrator.Orchestrator import default_orchestrator
from orchestrator.PhoenicisWinePackageCreationTask import PhoenicisWinePackageCreationTask

storage_api = Blueprint('storage_api', __name__)
packageStore = PackageStore()

@storage_api.route("/storage/logs/<distribution>")
def storage_logs(distribution):
    return jsonify(packageStore.fetch_versions(distribution))

@storage_api.route("/storage/binaries/<distribution>")
def storage_binaries(distribution):
    return jsonify(packageStore.fetch_versions(distribution))

@storage_api.route("/storage/logs/<distribution>/<log_file>")
def storage_log(distribution, log_file):
    return send_file(packageStore.fetch_log_name(distribution, log_file), attachment_filename=log_file, mimetype='text/plain')

@storage_api.route("/storage/binaries/missing/<distribution>")
def storage_missing_binaries(distribution):
    return jsonify(packageStore.fetch_missing_versions(distribution))

@storage_api.route("/storage/binaries/missing/<distribution>/autobuild")
def storage_missing_binaries_autobuild(distribution):
    for version in packageStore.fetch_missing_versions(distribution):
        distribution_name = distribution.split("-")[0]
        os = distribution.split("-")[1]
        arch = distribution.split("-")[2]
        wine_package_creation_task = PhoenicisWinePackageCreationTask(distribution_name, os, version, arch)
        default_orchestrator.run_task(wine_package_creation_task)
    return jsonify({"status": "ok"})

@storage_api.route("/storage/binaries/<distribution>/<binary_file>")
def storage_binary(distribution, binary_file):
    return send_file(packageStore.fetch_binary_name(distribution, binary_file), attachment_filename=binary_file, mimetype='application/gzip')