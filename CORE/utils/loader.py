from pathlib import Path


class Loader:
    """_summary_
        Clase encargada de cargar consultas SQL desde archivos ubicados en la carpeta "queries". Esta clase proporciona un método para leer el contenido de un archivo SQL y devolverlo como una cadena de texto, lo que facilita la ejecución de consultas en la base de datos.   
    
    Attributes:
        logger (logging.Logger): Instancia de logger para registrar eventos y errores durante la carga de
        consultas SQL.
        BASE_DIR (Path): Ruta base del directorio donde se encuentran los archivos SQL, estable
        cida al momento de crear una instancia de la clase Loader.
    
    Methods:
        load_query(query_name: str) -> str:
            Carga el contenido de un archivo SQL desde la carpeta "queries" y lo devuelve como una cadena de texto. Si el archivo no existe, se lanza una excepción FileNotFoundError.
        list_querys(querys: list) -> dict:
            Obtiene una lista de consultas SQL disponibles en el directorio de consultas y las carga utilizando la función load_query, devolviendo un diccionario con los nombres de las consultas como claves y su contenido como valores.
    """
    
    def __init__(self, logger, dir: Path):
        self.logger = logger
        self.BASE_DIR = dir
    
    def load_query(self, query_name: str) -> str:
        """_summary_
            Carga el contenido de un archivo SQL desde la carpeta "queries" ubicada en el directorio establecido en la intancia de la clase.
        Args:
            query_name (str): Nombre del archivo SQL que se desea cargar, incluyendo la extensión .sql

        Raises:
            FileNotFoundError: Si el archivo SQL no existe en la ruta especificada, se lanza una excepción indicando que no se encontró el archivo.

        Returns:
            str: El contenido del archivo SQL como una cadena de texto, que puede ser utilizada para ejecutar consultas en la base de datos.
        """
        query_path = self.BASE_DIR / "queries" / query_name
        
        if not query_path.exists():
            self.logger.error(f"No existe el archivo SQL: {query_path}")
            raise FileNotFoundError(
                f"No existe el archivo SQL: {query_path}"
            )
        
        return query_path.read_text(encoding="utf-8")
    
    def list_querys(self, querys: list) -> dict:
        """_summary_
            Obtiene una lista de consultas SQL disponibles en el directorio de consultas y las carga utilizando la función load_query.
        Args:
            querys (list): Lista con los nombres de las consultas SQL que se desean cargar, incluyendo la extensión .sql
        Returns:
            dict: Diccionario con los nombres de las consultas como claves y su contenido como valores.
        """
        scripts = {}
        # Cargamos el contenido de cada consulta usando la función load_query
        try:
            for q in querys:
                script= self.load_query(q)
                scripts[q] = script
                
            self.logger.info("Consultas listadas con éxito.")
            self.logger.info(f"Consultas disponibles: {querys}")
            return scripts
        except Exception as e:
            self.logger.error(f"Error al listar consultas: {e}")
            raise