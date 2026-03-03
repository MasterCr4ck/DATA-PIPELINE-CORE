from CORE.CONFIG.settings import get_connection_config
from CORE.DATABASE.postgres import PostgresDatabase
from CORE.DATABASE.mysql import MySQLDatabase
from CORE.DATABASE.mssql import MSSQLDatabase

def get_database(connection_name: str, env: str, pipeline: str):

    config = get_connection_config(connection_name, env)
    engine = config["engine"]

    if engine == "postgres":
        return PostgresDatabase(config, pipeline)

    elif engine == "mysql":
        return MySQLDatabase(config, pipeline)

    elif engine == "mssql":
        return MSSQLDatabase(config, pipeline)

    else:
        raise ValueError(f"Unsupported engine: {engine}")
