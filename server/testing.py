from data.database_sql import database_cls as database

db = database()

db.create_tables()

db.exit()