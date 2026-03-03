from CORE.LOGGING.logger import get_logger
from CORE.PIPELINES.metadata import BasePipelineMetadata
from CORE.DBLOG.Db_log import DBLog

class BasePipeline:
    def __init__(self, source_db, target_db, logger,metadata:BasePipelineMetadata):
        self.logger = logger
        self.source = source_db
        self.target = target_db
        self.metadata = metadata
        self.dblog = DBLog(self.target, logger)
        self.start_execution()
        
    list_queries = []
    
    querys = {}
    def start_execution(self):
        """_summary_
            Método para registrar el inicio de la ejecución del pipeline en la base de datos de logs. Aquí se puede utilizar la clase DBLog para insertar un registro en la tabla de logs con la información del pipeline, como el nombre, la versión, el autor, la frecuencia, la fecha de creación y el tiempo de ejecución.
        """
        self.execution_id = self.dblog.start_pipeline(self.metadata)
    
    def end_execution(self):
        """_summary_
            Método para registrar el fin de la ejecución del pipeline en la base de datos de logs. Aquí se puede utilizar la clase DBLog para insertar un registro en la tabla de logs con la información de la ejecución, como el nombre del pipeline, la versión, el autor, la frecuencia, la fecha de creación y el tiempo de ejecución.
        """
        self.dblog.end_pipeline(True)
    
    def extract(self):
        raise NotImplementedError

    def transform(self, df):
        return df

    def load(self, df):
        raise NotImplementedError
    
    def load_dataframe(self, df, table_name,if_exists ,schema=None):
        """_summary_
            
            Carga un DataFrame en una tabla de la base de datos destino utilizando SQLAlchemy.
        Args:
            df (_type_): DataFrame que se desea cargar en la base de datos
            table_name (_type_): Nombre de la tabla en la base de datos destino donde se cargarán los datos
            schema (_type_, optional): Esquema de la base de datos destino. Si no se especifica, se utilizará el esquema predeterminado. Defaults to None.
        """
        
        '''  
            if_exists

            "append" → agrega registros

            "replace" → borra tabla y la crea de nuevo

            "fail" → error si existe

            En pipelines productivos casi siempre usamos: append
        '''
        try:
            self.logger.info(f"Cargando DataFrame en la tabla {table_name} del esquema {schema}...")
            df.to_sql(
                name=table_name,
                con=self.target,          # <- engine
                schema=schema,            # opcional
                if_exists= if_exists,       # append | replace | fail
                index=False,
                chunksize=1000,           # carga por lotes
                method=None               
            )
            self.dblog.log_step(
                script_name=f"LOAD::{table_name}",
                est=True
            )

            self.logger.info(f"Carga completada correctamente en {table_name}.")

        except Exception as e:
            self.dblog.log_step(
                script_name=f"LOAD::{table_name}",
                est=False,
                obsv=str(e)
            )
            self.logger.error(f"Error en la carga: {e}")
            raise
        
    def list_querys(self):
        """_summary_
            Método para listar las consultas SQL disponibles para el pipeline. Aquí se pueden definir las consultas que se utilizarán en el proceso de extracción de datos, y se pueden cargar utilizando la clase Loader para facilitar su uso en el pipeline.
        """
        raise NotImplementedError