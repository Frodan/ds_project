import requests

# Для GET запросов пиши curl -i http://localhost:5000/file/info_file/123 - корень
# curl -i http://localhost:5000/file/delete_file/test1/123 - с субдиректорией


def test_upload_file():
    filename = 'test_file'
    with open(filename) as fp:
        content = fp.read()

    url = f"http://localhost:5000/file/upload_file/{filename}"
    response = requests.post(url, data=content)
    print(response)


def test_copy_file(): #
    filename = 'test_file'

    url = f"http://localhost:5000/file/copy_file/"
    data = {
        "from": filename,
        "to": f"check/{filename}"
    }
    response = requests.post(url, data=data)
    print(response.text)


def test_move_file():
    filename = 'test_file'

    url = f"http://localhost:5000/file/move_file/"
    data = {
        "from": filename,
        "to": f"check/moved_file"
    }
    response = requests.post(url, data=data)
    print(response.text)

#test_upload_file()
#test_copy_file()
#test_move_file()
