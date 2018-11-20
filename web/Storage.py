import io

from flask import Blueprint, jsonify, send_file

from storage.PackageStore import PackageStore

storage_api = Blueprint('storage_api', __name__)
packageStore = PackageStore()

@storage_api.route("/storage/logs/<distribution>")
def storage_logs(distribution):
    return jsonify(packageStore.fetch_logs(distribution))

@storage_api.route("/storage/logs/<distribution>/<log_file>")
def storage_log(distribution, log_file):
        return send_file(packageStore.fetch_log_name(distribution, log_file), attachment_filename=log_file, mimetype='text/plain')

@storage_api.route("/storage/binaries/<distribution>/<binary_file>")
def storage_log(distribution, binary_file):
        return send_file(packageStore.fetch_binary_name(distribution, binary_file), attachment_filename=binary_file, mimetype='application/gzip')