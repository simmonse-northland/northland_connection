from sqlalchemy import create_engine, text

from config import DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE
import os

server = DB_SERVER
username = DB_USERNAME
password = DB_PASSWORD
database = DB_DATABASE

def connect(db):
    engine = create_engine(f"mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{db}")
    return engine

from sqlalchemy.orm import sessionmaker

def execute_query(db, sql, params=None):
    engine = connect(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        if params:
            result = session.execute(text(sql), params)
        else:
            result = session.execute(text(sql))
        session.commit()
        return result.fetchall()
    except:
        session.rollback()
        raise
    finally:
        session.close()
