from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from CORE.DATABASE.base import base

class MySQLDatabase(base):
    
    def get_engine(self):

        driver = self.config.get("driver", "pymysql")

        user = quote_plus(self.config["user"])
        password = quote_plus(self.config["password"])

        connection_url = (
            f"mysql+{driver}://{user}:{password}"
            f"@{self.config['host']}:{self.config['port']}"
            f"/{self.config['database']}"
        )

        return create_engine(
            connection_url,
            pool_pre_ping=True
        )
    
    def test(self):
        """
        Prueba de conexión específica a MySQL
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            self.logger.error(f"Error MySQL: {e}")
            return False
    def insertar_datos(self, query: str, params: list[dict] = None):
        """
        Método para insertar datos en el warehouse.
        
        Args:
            query (str): Consulta SQL de inserción.
            params (list[dict]): Parámetros para la consulta SQL.
        """
        with self.engine.begin() as conn:
            conn.execute(text(query), params)