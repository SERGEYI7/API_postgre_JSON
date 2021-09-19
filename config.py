import json


class TypeDBError(Exception):
    def __str__(self):
        return "Неверный тип БД"


def write_param(user, password, host, port, dbname, type_db):
    """
    Сохранение настроек в файле JSON для соединения сервера postgres
    :param user:
    :param password:
    :param host:
    :param port:
    :param dbname:
    :param type_db: тут доступны только 2 варианта JSON и postgres
    :return:
    """
    if type_db == 'JSON' or type_db == 'postgres':
        with open('config.json', 'w') as file:
            json.dump({'user': user, 'password': password, 'host': host,
                       'port': port, 'dbname': dbname, 'type_db': type_db}, file)
    else:
        raise TypeDBError


def read_param():
    """
    Прочесть настройки из JSON файла
    :return: словарь с текущими настройками
    """
    with open('config.json', 'r') as file:
        return json.load(file)
