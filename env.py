import os


db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")
db_host = os.getenv("DB_HOST")

db_dsn = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
system_db_dsn = os.getenv("SYSTEM_DB_DSN")