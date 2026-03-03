
from CORE.PIPELINES.metadata import BasePipelineMetadata
from CORE.utils.loader import Loader

class MainPipeline:
    def __init__(self, logger, metadata:BasePipelineMetadata,pipeline_name):
        self.logger = logger
        self.metadata = metadata
        self.pipeline_name = pipeline_name
        self.metadata.log_metadata(self.logger)
        self.logger.info(f"Pipeline {self.pipeline_name} iniciado.", extra={"stage": "START"})
        
        
    def run(self):
        """_summary_
            Método principal para ejecutar el pipeline. Aquí se establecen los parametros para la ejecución del pipeline, se inician las conexiones a las bases de datos, se ejecuta el pipeline específico y se manejan los logs de inicio y fin de la ejecución.
        """
        raise NotImplementedError
        
    def start_Conection(self):
        """_summary_
            Método para iniciar las conexiones a las bases de datos. Aquí se pueden configurar las conexiones a diferentes motores de base de datos según sea necesario.
        """
        raise NotImplementedError
    
    def prepare_dates(self):
        """_summary_
            Método para preparar las fechas de inicio y fin para la extracción de datos. Aquí se pueden configurar las fechas según la frecuencia del pipeline (diaria, semanal, mensual, etc.) y el rango de datos que se desea procesar.
        """
        raise NotImplementedError