from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from environs import Env
env = Env()
env.read_env('.local.env')
db_url = env('DB_URL')
engine = create_engine(f"{db_url}")

Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session 

