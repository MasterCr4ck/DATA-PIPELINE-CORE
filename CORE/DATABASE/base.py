from abc import ABC, abstractmethod
from CORE.LOGGING.logger import get_logger


class base(ABC):

    def __init__(self, config,namePipeline: str):
        self.config = config
        self.logger = get_logger(
            name=__name__,
            pipeline=namePipeline,
            log_file=f"logs/{namePipeline}.log"
        )
        self.engine = self.get_engine()
        

    @abstractmethod
    def get_engine(self):
        """_summary_
        """
        pass
    
    def start_connection(self):
        """_summary_
        Establece la conexión a la base de datos y verifica su validez.
        Raises:
            ConnectionError: Si no se puede establecer la conexión.

        Returns:
            engine: SQLAlchemy Engine object
        """
        self.logger.info("Estableciendo conexion", extra={"config": self.config})
        if self.test():
            self.logger.info("Test de conexion exitoso.")
            return self.engine
        else:
            self.logger.error("Error al conectar a la base de datos.")
            raise ConnectionError("No se pudo establecer conexión.")
        
    @abstractmethod
    def test(self):
        """
        Cada motor debe implementar su propia conexión
        """
        pass
