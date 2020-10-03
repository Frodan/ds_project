import os
import shutil
from flask import Flask, request, jsonify, send_from_directory
from flask import Response

UPLOAD_DIRECTORY = "/home/user/files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)


@api.route("/dir/make_dir/<path:path>")
def make_directory(path):
    """Make a directory"""
    directory = os.path.join(UPLOAD_DIRECTORY, path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        return Response("{'Status':'Success'}", status=200, mimetype='application/json')
    else:
        return Response("{'Status':'directory already existed'}", status=400, mimetype='application/json')


@api.route("/dir/delete_dir/<path:path>")
def delete_directory(path):
    """Delete a directory"""
    directory = os.path.join(UPLOAD_DIRECTORY, path)
    if not os.path.exists(directory):
        return Response("{'Status':'Directory does not exist'}", status=400, mimetype='application/json')
    else:
        shutil.rmtree(directory, ignore_errors=True)
        return Response("{'Status':'Success'}", status=200, mimetype='application/json')


@api.route("/dir/list_dir/")
@api.route("/dir/list_dir/<path:path>")
def list_files(path=''):
    """List files in choosen dir at the server."""
    if not path:
        directory = UPLOAD_DIRECTORY
    else:
        directory = os.path.join(UPLOAD_DIRECTORY, path)
    if not os.path.exists(directory):
        return Response("{'Status':'Directory does not exist'}", status=400, mimetype='application/json')
    files = []
    directories = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            files.append(filename)
        else:
            directories.append(filename)
    result = {"files": files, "directories": directories}
    return jsonify(result)


@api.route("/file/make_file/<path:path>")
def make_file(path):
    """Touch a file"""
    file_path = os.path.join(UPLOAD_DIRECTORY, path)
    check = file_path.split("/")
    directory = "/".join(check[:-1])
    if not os.path.exists(directory):
        return Response("{'Status':'Directory does not exist'}", status=400, mimetype='application/json')
    else:
        if os.path.exists(file_path):
            return Response("{'Status':'File with such name already exist'}", status=400, mimetype='application/json')
        else:
            open(file_path, 'a').close()
            return Response("{'Status':'Success'}", status=200, mimetype='application/json')


@api.route("/file/read_file/<path:path>")
def read_file(path):
    """Read a file"""
    file_path = os.path.join(UPLOAD_DIRECTORY, path)
    if not os.path.exists(file_path):
        return Response("{'Status':'File does not exits'}", status=400, mimetype='application/json')
    else:
        return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/file/delete_file/<path:path>")
def delete_file(path):
    """Delete a file"""
    file_path = os.path.join(UPLOAD_DIRECTORY, path)
    if os.path.exists(file_path):
        os.remove(file_path)
        return Response("{'Status':'Success'}", status=200, mimetype='application/json')
    else:
        return Response("{'Status':'File does not exist'}", status=400, mimetype='application/json')


@api.route("/file/upload_file/<path:path>", methods=["POST"])
def post_file(path):
    """Upload a file."""
    file_path = os.path.join(UPLOAD_DIRECTORY, path)
    check = file_path.split("/")
    directory = "/".join(check[:-1])
    if not os.path.exists(directory):
        return Response("{'Status':'Directory does not exist'}", status=400, mimetype='application/json')
    else:
        with open(os.path.join(UPLOAD_DIRECTORY, path), "wb") as fp:
            fp.write(request.data)
            return Response("{'Status':'Success'}", status=200, mimetype='application/json')


@api.route("/file/copy_file/", methods=["POST"])
def copy_file():
    file_from = os.path.join(UPLOAD_DIRECTORY, request.form.get('from'))
    file_to = os.path.join(UPLOAD_DIRECTORY, request.form.get('to'))

    from_dir = "/".join(file_from.split('/')[:-1])
    to_dir = "/".join(file_to.split('/')[:-1])

    if not os.path.exists(from_dir):
        return Response("{'Status':'From directory does not exist'}", status=400, mimetype='application/json')
    elif not os.path.exists(to_dir):
        return Response("{'Status':'To directory does not exist'}", status=400, mimetype='application/json')
    elif not os.path.exists(file_from):
        return Response("{'Status':'File does not exist'}", status=400, mimetype='application/json')
    else:
        shutil.copy(file_from, file_to)
        return Response("{'Status':'Success'}", status=200, mimetype='application/json')


@api.route("/file/move_file/", methods=["POST"])
def move_file():
    file_from = os.path.join(UPLOAD_DIRECTORY, request.form.get('from'))
    file_to = os.path.join(UPLOAD_DIRECTORY, request.form.get('to'))

    from_dir = "/".join(file_from.split('/')[:-1])
    to_dir = "/".join(file_to.split('/')[:-1])

    if not os.path.exists(from_dir):
        return Response("{'Status':'From directory does not exist'}", status=400, mimetype='application/json')
    elif not os.path.exists(to_dir):
        return Response("{'Status':'To directory does not exist'}", status=400, mimetype='application/json')
    elif not os.path.exists(file_from):
        return Response("{'Status':'File does not exist'}", status=400, mimetype='application/json')
    else:
        shutil.move(file_from, file_to)
        return Response("{'Status':'Success'}", status=200, mimetype='application/json')


@api.route("/file/info_file/<path:path>")
def info_file(path):
    """Get info about a file"""
    file_path = os.path.join(UPLOAD_DIRECTORY, path)
    if os.path.exists(file_path):
        stats = os.stat(file_path)
        info ={
            "size": stats.st_size,
            "recent access": stats.st_atime,
            "recent modification": stats.st_mtime
        }
        return jsonify(info)
    else:
        return Response("{'Status':'File does not exist'}", status=400, mimetype='application/json')


if __name__ == "__main__":
    api.run(debug=True, port=8000)