import sqlparse
from models.db import app_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
import setup_admin
if __name__== '__main__':
    sql_commands_str: str
    with open('raw_sql_db_test.sql', 'r') as sql_f:
        sql_commands_str = sql_f.read()
    sql_commands = sqlparse.parse(sql_commands_str)
    session: Session
    with app_engine().Session() as session:
        try:
            for command in sql_commands:
                session.execute(text(str(command)))
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error has occured:\n\t{e}")
        else:
            print('Adding sample username \'admin\' with password \'password\'')
            try:
                setup_admin.setup_admin(option='r', username='admin')
            except Exception as e:
                print(e)
            setup_admin.setup_admin(option='a', username='admin', password='password')