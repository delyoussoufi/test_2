import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

from flaskapp.config import DevelopmentTestConfig
from resources.sql import sql_path

create_sql_file = 'create_schema.sql'
data_sql_file = 'data.sql'

class DbTestUtils:

    @staticmethod
    def create_database_tables():
        commands = DbTestUtils.split_sql_file_commands(create_sql_file)
        commands.extend(DbTestUtils.split_sql_file_commands(data_sql_file))

        engine = create_engine(DevelopmentTestConfig.SQLALCHEMY_DATABASE_URI, isolation_level='AUTOCOMMIT')

        # adapted to work with sqlalchemy > 2
        with engine.connect() as conn:
            if len(commands) > 0:
                for command in commands:
                    conn.execute(text(command))

        engine.dispose()

    @staticmethod
    def split_sql_file_commands(sql_file: str):
        sql_file_path = os.path.join(sql_path, sql_file)
        with open(sql_file_path, 'r') as f:
            return [f"{stm};" for stm in f.read().split(";")]

