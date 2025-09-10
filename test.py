from my_postgresql import MyDB

my_db = MyDB()
my_db.connect()

print(my_db.db_version())

my_db.close()