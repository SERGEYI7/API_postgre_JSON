import psycopg2
import json
from json import JSONDecodeError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBJSON:

    def __init__(self):
        self.free_id = list()
        try:
            with open('user.json', 'r+', encoding='utf-8') as file:
                self.r_json = json.load(file)
        except JSONDecodeError:
            with open('user.json', 'w', encoding='utf-8') as file:
                json.dump({}, file)
        with open('user.json', 'r+', encoding='utf-8') as file:
            self.r_json = json.load(file)
        self.check()

    def check(self):
        """
        Проверка файла БД на ошибки и исправления их
        И автоматическое создание уникального id
        """
        index_iter = set()
        id_in_db = set()
        if len(self.r_json) == 0:
            self.free_id.append(1)
        else:
            for index, item in enumerate(self.r_json.items()):
                index_iter.add(index+1)
                id_in_db.add(int(item[0]))
        formatting_set = list(index_iter.difference(id_in_db))
        if len(formatting_set) == 0 and len(self.r_json) > 0:
            self.free_id.append(int(max(id_in_db))+1)
        else:
            if len(self.r_json) > 0:
                self.free_id.append(formatting_set[0])

    def insert(self, fio):
        """
        Создание новой строки в БД с указанным fio
        :param fio:
        """
        with open('user.json', 'w', encoding='utf-8') as file:
            self.check()
            var_dict = self.r_json
            var_dict[self.free_id[0]] = fio
            # self.free_id.pop(0)
            json.dump(var_dict, file, ensure_ascii=False)

    def update(self, id, fio):
        """
        Обновление указанной строки
        :param id: id строки
        :param fio: Обновленный fio
        """
        with open('user.json', 'w', encoding='utf-8') as file:
            var_dict = self.r_json
            var_dict[id] = fio
            json.dump(var_dict, file, ensure_ascii=False)

    def get(self, id=None):
        """
        Получение строки с конкретным БД или всей базы данных
        :param id: id нужной строки в БД
        :return: Возвращает всю БД при id=None, или конкретную строку с указанным id
        """
        if id is None:
            return self.r_json
        else:
            return self.r_json[id]

    def delete(self, id):
        """
        Удаление строки в БД с указанным id
        :param id:
        """
        with open('user.json', 'w', encoding='utf-8') as file:
            var_dict = self.r_json
            var_dict.pop(id)
            json.dump(var_dict, file, ensure_ascii=False)


class DBPostgres:

    def __init__(self, user, password, host, port, dbname):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.connection = None
        self.cursor = None
        self.settings_connect()

    def settings_connect(self):
        try:
            self.connection = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                               port=self.port)
        except Exception as error:
            print(error)

    def connect(self):
        """
        Проверка на присутствие введенного имени БД в self.bd_name и таблицы
        При их отсутсвии они автоматически создаются и подключаются
        :return:
        """
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()
        self.cursor.execute(r'SELECT datname FROM pg_database')
        all_databases = self.cursor.fetchall()
        for index, item in enumerate(all_databases):
            if len(all_databases) == index+1 and item != (self.dbname,):
                sql_create_drop_database = f'CREATE DATABASE {self.dbname}'  # 'DROP DATABASE Test_DB'
                self.cursor.execute(sql_create_drop_database)
                print(f'Create new DataBase "{self.dbname}"')
                self.connection.close()
                self.cursor.close()
                self.connection = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                                   port=self.port, database=self.dbname)
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                self.cursor = self.connection.cursor()
                print(f'Connect to {self.dbname}')
                # self.cursor.execute(r'\CONNECT test_db')
                self.cursor.execute('''CREATE TABLE "user" (
                                        id SERIAL PRIMARY KEY,
                                        fio TEXT
                                        )
                                     ''')
                # self.connection.commit()
            elif item == (self.dbname,):
                self.connection.close()
                self.cursor.close()
                self.connection = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                                   port=self.port, database=self.dbname)
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                self.cursor = self.connection.cursor()

    def insert_line_db(self, fio):
        """
        Creating a new line in DB
        :param fio: Фамилия Имя Отчество
        :return: None
        """
        self.cursor.execute(f"INSERT INTO \"user\" (fio) VALUES (\'{fio}\')")

    def delete_line_db(self, id):
        """
        delete line in db
        :param id: id user
        :return:
        """
        self.cursor.execute(f"DELETE FROM \"user\" WHERE id = \'{id}\'")

    def update_line_db(self, id, fio):
        """
        update line in db
        :param id: id user
        :param fio: Фамилия Имя Отчество
        :return:
        """
        self.cursor.execute(f"UPDATE \"user\" SET fio = \'{fio}\' WHERE id = \'{id}\'")

    def get_line_db(self, id):
        """
        get line in db
        :param id: id user
        :return:
        """
        command = f"SELECT * FROM \"user\" WHERE id = \'{id}\'"
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def get_all_lines(self):
        """
        :return: all lines in db
        """
        self.cursor.execute(f"SELECT * FROM \"user\"")
        return self.cursor.fetchall()
