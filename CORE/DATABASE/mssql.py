from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from CORE.DATABASE.base import base

class MSSQLDatabase(base):

    def get_engine(self):

        connection_string = (
             f"DRIVER={{{self.config['driver']}}};"
            f"SERVER={self.config['host']},{self.config['port']};"
            f"DATABASE={self.config['database']};"
            f"UID={self.config['user']};"
            f"PWD={self.config['password']};"
            f"TrustServerCertificate=yes;"
        )

        connection_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"

        return create_engine(connection_url)
    
    def test(self):
        """
        Prueba de conexión específica a SQL Server
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT GETDATE()"))
            return True
        except Exception as e:
            self.logger.error(f"Error SQL Server: {e}")
            return False