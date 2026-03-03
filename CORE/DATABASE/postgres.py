from sqlalchemy import create_engine, text
from CORE.DATABASE.base import base

class PostgresDatabase(base):

    def get_engine(self):
        return create_engine(
            f"postgresql+psycopg2://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        )
    def test(self):
        """
        Prueba de conexión específica a PostgreSQL
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            self.logger.error(f"Error PostgreSQL: {e}")
            return False