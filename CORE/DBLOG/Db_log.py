import pandas as pd
import sqlalchemy as sa
from datetime import datetime

class DBLog:

    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger
        self.execution_id = None
        self.cons = 0

    # ===============================
    # MASTER LOG
    # ===============================
    def start_pipeline(self, metadata):
        """_summary_
            Registra el inicio de la ejecución del pipeline en la base de datos de logs.
        Args:
            metadata (BasePipelineMetadata): Objeto que contiene la información del pipeline, como el nombre, la versión, el autor, la frecuencia y la fecha de creación.
        Returns:
            int: ID de la ejecución registrada en la base de datos de logs.
        """
        query = sa.text("""
            INSERT INTO LogPipeline
            (Pipel, PipeV, CoreV, FchReg, Est)
            VALUES (:pipel, :pipev, :corev, :fchreg, 0)
        """)

        with self.engine.begin() as conn:
            result = conn.execute(
                query,
                {
                    "pipel": metadata.name,
                    "pipev": metadata.version,
                    "corev": metadata.core_version,
                    "fchreg": datetime.now()
                }
            )
            
            self.execution_id = result.lastrowid

        self.logger.info(
            f"Execution registrada con ID={self.execution_id}"
        )

        return self.execution_id
    
    def log_step(self, script_name, est=True, obsv=None):
        """_summary_
            Registra un paso especifico del pipeline en la base de datos de logs.
        Args:
            script_name (str): Nombre del paso o script que se está registrando.
            est (bool, optional): Estado del paso (True para éxito, False para error). Defaults to True.
            obsv (str, optional): Observaciones adicionales sobre el paso. Defaults to None.
        Returns:
            None
        """
        
        self.cons += 1

        query = sa.text("""
            INSERT INTO Logpipeline1
            (Id, Cons, ScriptName, Est, Obsv)
            VALUES (:id, :cons, :script, :est, :obsv)
        """)

        with self.engine.begin() as conn:
            conn.execute(
                query,
                {
                    "id": self.execution_id,
                    "cons": self.cons,
                    "script": script_name,
                    "est": est,
                    "obsv": obsv
                }
            )
            
    def end_pipeline(self, success=True):
        """_summary_
            Registra el fin de la ejecución del pipeline en la base de datos de logs.
        Args:
            success (bool, optional): Indica si la ejecución del pipeline fue exitosa o no. Defaults to True.
        Returns:
            None
        """

        query = sa.text("""
            UPDATE LogPipeline
            SET Est = :est
            WHERE Id = :id
        """)

        with self.engine.begin() as conn:
            conn.execute(
                query,
                {"est": success, "id": self.execution_id}
            )

        self.logger.info("Pipeline finalizada correctamente",extra={"stage": "END"})            