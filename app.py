from fastapi import FastAPI
from json import JSONDecodeError
import db_control
import config

app = FastAPI()
read_param = config.read_param()
if read_param['type_db'] == 'postgres':
    try:
        db = db_control.DBPostgres(user=read_param['user'], password=read_param['password'], host=read_param['host'],
                                   port=read_param['port'], dbname=read_param['dbname'])
        db.connect()
    except JSONDecodeError:
        print('Файл config.json пустой.')


@app.get("/")
async def get_users(id=None):
    if read_param['type_db'] == 'postgres':
        if id is not None and id.isdigit():
            return db.get_line_db(id)
        elif id is None:
            return db.get_all_lines()
    elif read_param['type_db'] == 'JSON':
        return db_control.DBJSON().get(id)


@app.post("/")
async def append_user(fio):
    if read_param['type_db'] == 'postgres':
        db.insert_line_db(fio)
    elif read_param['type_db'] == 'JSON':
        return db_control.DBJSON().insert(fio)


@app.patch("/")
async def patch_user(id, fio):
    if read_param['type_db'] == 'postgres':
        db.update_line_db(id, fio)
    elif read_param['type_db'] == 'JSON':
        return db_control.DBJSON().update(id, fio)


@app.delete("/")
async def delete_user(id):
    if read_param['type_db'] == 'postgres':
        # db.connect()
        db.delete_line_db(id)
    elif read_param['type_db'] == 'JSON':
        return db_control.DBJSON().delete(id)
