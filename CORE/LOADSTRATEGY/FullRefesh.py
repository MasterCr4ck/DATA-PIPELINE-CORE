import sqlalchemy
from CORE.DBLOG.Db_log import DBLog

class FullRefresh:

    def __init__(self, logger,dblog:DBLog):
        self.logger = logger
        self.dblog = dblog

    def execute(self, engine, delete_sql, insert_sql,script_name_delete,script_name_insert):
        self.logger.info("Iniciando full refresh...")
        try:
            with engine.begin() as conn:
                conn.execute(sqlalchemy.text(delete_sql))
                conn.execute(sqlalchemy.text(insert_sql))

            self.logger.info("Full refresh ejecutado correctamente.")
            self.dblog.log_step(
                script_name=f"FULL_REFRESH::{script_name_delete} & {script_name_insert}",
                est=True
            )

        except Exception as e:
            self.logger.error(f"Error en full refresh: {e}")
            self.dblog.log_step(
                script_name=f"FULL_REFRESH::{script_name_delete} & {script_name_insert}",
                est=False,
                obsv=str(e)
            )
            raise
