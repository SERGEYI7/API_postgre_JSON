import requests


def get_line_db(id=None):
    r_users = requests.get('http://localhost:8080/', params={'id': id})
    return r_users.text


def patch_line_db(id, fio):
    requests.patch('http://localhost:8080/', params={'id': id, 'fio': fio})


def post_line_db(fio):
    requests.post('http://localhost:8080/', params={"fio": fio})


def delete_line_db(id):
    requests.delete('http://localhost:8080/', params={'id': id})


