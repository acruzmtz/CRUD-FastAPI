from peewee import *

connection = MySQLDatabase(
    'fastapi',
    user='root',
    passwd='1149',
    host='localhost'
)


class User(Model):
    """ Create model of database """
    username = CharField(max_length=50)
    email = CharField(max_length=50)

    def __str__(self):
        return self.username

    class Meta():
        database = connection
        table_name = 'users'
