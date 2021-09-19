import engine
import config

config.write_param(user='', password='', host='', port='', dbname='', type_db='')

# Получить все строки в БД
# print(engine.get_line_db())

# Получить строку по номеру id
# print(engine.get_line_db(5))

# Изменить ФИО в строке с заданным номером id
# engine.patch_line_db(10, "Игорь Иван Иваныч")

# Добавить нового user'а с заданным fio
# engine.post_line_db('Володин Дмитрий Сергеевич')

# Удалить строку
# engine.delete_line_db(3)
