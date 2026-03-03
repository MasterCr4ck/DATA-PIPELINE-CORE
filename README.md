
# DATA-PIPELINE-CORE

![green-divider](https://user-images.githubusercontent.com/7065401/52071924-c003ad80-2562-11e9-8297-1c6595f8a7ff.png)

## CONTENIDO

- [DATA-PIPELINE-CORE](#data-pipeline-core)
  - [CONTENIDO](#contenido)
  - [1 Descripción](#1-descripción)
  - [2 Estructura del proyecto](#2-estructura-del-proyecto)
  - [3 Concepto clave](#3-concepto-clave)
  - [4 Requisitos](#4-requisitos)
  - [5 Instalación del core](#5-instalación-del-core)
    - [5.1 Crear y activar un entorno virtual](#51-crear-y-activar-un-entorno-virtual)
    - [5.2 Instalar el core en modo editable](#52-instalar-el-core-en-modo-editable)
    - [5.3 Verificación rápida](#53-verificación-rápida)
  - [6 Uso desde un pipeline externo](#6-uso-desde-un-pipeline-externo)
    - [6.1 Ejemplo de estructura de pipelines](#61-ejemplo-de-estructura-de-pipelines)
    - [6.2 Instalación del core desde el pipeline](#62-instalación-del-core-desde-el-pipeline)
    - [6.3 Uso dentro del pipeline](#63-uso-dentro-del-pipeline)
  - [7 Módulos disponibles](#7-módulos-disponibles)
    - [7.1 Logging](#71-logging)
      - [Firma](#firma)
      - [Parámetros](#parámetros)
      - [Comportamiento interno](#comportamiento-interno)
        - [Nivel de logging](#nivel-de-logging)
        - [Evita duplicación de handlers](#evita-duplicación-de-handlers)
        - [Formateo personalizado](#formateo-personalizado)
        - [Uso de LoggerAdapter](#uso-de-loggeradapter)
      - [Uso recomendado dentro de un pipeline](#uso-recomendado-dentro-de-un-pipeline)
      - [Buenas prácticas](#buenas-prácticas)
    - [7.2 Configuración](#72-configuración)
    - [7.3 Base de datos](#73-base-de-datos)
      - [Uso desde un pipeline](#uso-desde-un-pipeline)
      - [Motores soportados](#motores-soportados)
  - [8 Buenas prácticas](#8-buenas-prácticas)
  - [9 Versionado](#9-versionado)
  - [10 Novedades — Versión 2.0.0](#10-novedades--versión-200)
    - [10.1 Nuevo módulo DBLOG](#101-nuevo-módulo-dblog)
    - [10.2 Estandarización mediante `main_pipeline`](#102-estandarización-mediante-main_pipeline)
    - [10.3 Mejora en `PipelineLoggerAdapter`](#103-mejora-en-pipelineloggeradapter)
    - [10.4 Ajustes en estrategia `FullRefresh`](#104-ajustes-en-estrategia-fullrefresh)
    - [10.5 Nueva utilidad: Loader de Queries](#105-nueva-utilidad-loader-de-queries)
    - [10.6 Utilities reutilizables ampliadas](#106-utilities-reutilizables-ampliadas)
    - [10.7 Enfoque arquitectónico de la versión 2.0.0](#107-enfoque-arquitectónico-de-la-versión-200)
    - [10.8 Cambios incompatibles (Breaking Changes)](#108-cambios-incompatibles-breaking-changes)
    - [10.9 Migración recomendada](#109-migración-recomendada)
  - [11 Autor](#11-autor)


## 1 Descripción

**DATA-PIPELINE-CORE** es un core reutilizable para la construcción de pipelines de datos en Python.

Centraliza funcionalidades comunes como:

- Logging estandarizado
- Configuración por entorno
- Conexiones a bases de datos (definidas por YAML)
- Utilidades compartidas

El objetivo es:

- Evitar duplicación de código
- Garantizar consistencia entre pipelines
- Facilitar mantenimiento y escalabilidad
- Separar lógica de negocio del framework base

## 2 Estructura del proyecto

``` TXT
DATA-PIPELINE-CORE/
│
├── setup.py
├── requirements.txt
├── README.md
│
└── core/
    ├── __init__.py
    │
    ├── logging/
    │   ├── __init__.py
    │   └── logger.py
    │
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    │
    ├── database/
    │   ├── __init__.py
    │   └── connection.py
    │
    └── utils/
        ├── __init__.py
        └── helpers.py

```

## 3 Concepto clave

Este repositorio NO es un pipeline, es una librería interna que los pipelines instalan y reutilizan.

Los pipelines viven en repositorios o carpetas separadas y consumen este core vía ``` pip install -e.```

## 4 Requisitos

- Python 3.9+
- pip
- Entorno virtual (obligatorio en entornos profesionales)

## 5 Instalación del core

### 5.1 Crear y activar un entorno virtual

``` bash
python -m venv .venv
.\\.venv\Scripts\activate
```
Es fundamental que tanto el Core como los pipelines utilicen el mismo entorno virtual.
### 5.2 Instalar el core en modo editable

Desde el repositorio DATA-PIPELINE-CORE:

``` bash
pip install -e .
```

- Reflejar cambios sin reinstalar
- Reutilizar el Core en múltiples pipelines
- Mantener una sola fuente de verdad

Si se utiliza un IDE como Visual Studio Code, la activación puede gestionarse automáticamente, pero el entorno virtual debe existir y estar correctamente seleccionado.

### 5.3 Verificación rápida

``` bash
python -c "import core; print(core.\_\_file\_\_)"
```

Debe mostrar una ruta dentro de:

``` bash
DATA-PIPELINE-CORE/core
```

Si no es así, probablemente se está usando otro entorno virtual.

## 6 Uso desde un pipeline externo

### 6.1 Ejemplo de estructura de pipelines

``` txt
PIPELINES/
├── .venv/
│
├── DATA-PIPELINE-CORE/
│
├── pipeline-hospitalizacion-domiciliaria/
│
├── .venv/
├── requirements.txt
├── README.md
│
├── pipeline/
│   ├── __init__.py
│   ├── main.py
│   ├── pipeline.py
│   │
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── parameters.py
│   │   └── schemas.py
│   │
│   ├── queries/
│   │   ├── __init__.py
│   │   ├── extract.sql
│   │   └── load.sql
│   │
│   └── services/
│       ├── __init__.py
│       ├── extractor.py
│       ├── transformer.py
│       └── loader.py
│
├── data/
│   ├── input/
│   └── output/
│
└── logs/
```

Todos deben usar el mismo entorno virtual

### 6.2 Instalación del core desde el pipeline

``` bash
pip install -e ../DATA-PIPELINE-CORE
```

### 6.3 Uso dentro del pipeline

``` python 
from core.logging.logger import get_logger

logger = get_logger("hospitalizacion_domiciliaria")
logger.info("Pipeline iniciado correctamente")
```

## 7 Módulos disponibles

### 7.1 Logging

El Core implementa un sistema de logging centralizado orientado a pipelines, que permite:

- Estandarizar el formato de logs
- Identificar cada pipeline en los registros
- Registrar en consola y opcionalmente en archivo
- Evitar duplicación de handlers
- Mantener consistencia entre todos los pipelines

El logger se construye a través de la función:

```python
from CORE.LOGGING.logger import get_logger
```

#### Firma

```python

get_logger(
    name: str,
    pipeline: str = "GLOBAL",
    log_file: str | None = None
) -> logging.Logger

```

#### Parámetros

``` name: str ``` : Nombre interno del logger.

Normalmente se recomienda usar:

- Nombre del módulo
- Nombre del pipeline
- O ```__name__ ```

Ejemplo:

```python
logger = get_logger(name="hospitalizacion_main")
```

``` pipeline: str = "GLOBAL" ``` : Nombre del pipeline que aparecerá en el log.
Este valor se inyecta mediante logging.LoggerAdapter usando:

```python
extra={"pipeline": pipeline}
```

Esto permite que el PipelineFormatter incluya el nombre del pipeline dentro del formato del log.

Ejemplo:

```python
logger = get_logger(
    name="hospitalizacion",
    pipeline="hospitalizacion_domiciliaria"
)
```

Salida esperada (ejemplo conceptual):

```yaml
2026-02-20 14:12:03 | hospitalizacion_domiciliaria | INFO | Pipeline iniciado
```

Si no se especifica, se utiliza "GLOBAL".

```log_file: str | None = None ``` : Ruta opcional de archivo para registrar logs adicionales.
Si se define:

- Se agrega un FileHandler
- Se mantiene también el ConsoleHandler

Ejemplo:

```python
logger = get_logger(
    name="hospitalizacion",
    pipeline="hospitalizacion_domiciliaria",
    log_file="logs/hospitalizacion.log"
)
```

Esto generará:

- Logs en consola
- Logs persistidos en archivo

Si no se define, solo se registran en consola.

#### Comportamiento interno

##### Nivel de logging

```python
logger.setLevel(logging.INFO)
```

Nivel por defecto: INFO

Puede modificarse posteriormente si se requiere.

##### Evita duplicación de handlers

```python
if logger.handlers:
    return logger
```

Esto previene que al llamar varias veces get_logger se agreguen múltiples handlers al mismo logger.

##### Formateo personalizado

```python
PipelineFormatter(DEFAULT_FORMAT)
```

Este formatter:

- Extiende el comportamiento estándar de logging
- Incluye el nombre del pipeline en cada registro
- Mantiene un formato homogéneo en todos los pipelines

##### Uso de LoggerAdapter

El logger final no es un logging.Logger puro, sino:

```python
logging.LoggerAdapter(logger, extra={"pipeline": pipeline})
```

Esto permite:

- Inyectar contexto adicional
- Agregar el campo pipeline al formatter
- Mantener el código del pipeline limpio (sin pasar manualmente el pipeline en cada log)

#### Uso recomendado dentro de un pipeline

```python
from CORE.LOGGING.logger import get_logger

class PipelineHospitalizacion:

    def __init__(self):
        self.pipeline = "hospitalizacion_domiciliaria"
        self.logger = get_logger(
            name=self.pipeline,
            pipeline=self.pipeline,
            log_file="logs/hospitalizacion.log"
        )

    def run(self):
        self.logger.info("Pipeline iniciado")
```

#### Buenas prácticas

- Usar siempre el nombre del pipeline como parámetro pipeline
- No crear loggers manuales con logging.getLogger() fuera del Core
- No redefinir handlers en los pipelines
- Centralizar el formato únicamente en el Core

### 7.2 Configuración

Pensado para:

- Variables por entorno (dev, qa, prod)
- Archivos YAML
- Configuración desacoplada del código
- Definición de drivers y credenciales de base de datos desde YAML

Ejemplo conceptual de configuración:

```yaml
connections:
  operational_db:
    engine: mssql
    driver: ODBC Driver 17 for SQL Server
    host: Servidor
    port: 1433
    database: Database
    user: User
    password: Pass

  warehouse_db:
    engine: mysql
    driver: pymysql
    host: Servidor
    port: 3306
    database: Database
    user: User
    password: Pass

```

Uso:

``` python
from core.config.settings import settings
db_config = settings.database
```

### 7.3 Base de datos

El Core implementa un Factory Pattern para la creación de conexiones a base de datos.

Permite:

- Resolver dinámicamente el tipo de base de datos según YAML
- Mantener desacoplada la lógica de conexión
- Integrar automáticamente el logger del pipeline
- Centralizar configuración por entorno (dev, qa, prod)

La configuración de las bases de datos se define en el archivo YAML por entorno.

Entorno **dev** en archivo **database.dev.yaml**

```yaml
connections:
  operational_db:
    engine: mssql
    driver: ODBC Driver 17 for SQL Server
    host: Servidor
    port: 1433
    database: Database
    user: User
    password: Pass

  warehouse_db:
    engine: mysql
    driver: pymysql
    host: Servidor
    port: 3306
    database: Database
    user: User
    password: Pass

```

Entorno **prod** en archivo **database.prod.yaml**

```yaml
connections:
  operational_db:
    engine: mssql
    driver: ODBC Driver 17 for SQL Server
    host: Servidor
    port: 1433
    database: Database
    user: User
    password: Pass

  warehouse_db:
    engine: mysql
    driver: pymysql
    host: Servidor
    port: 3306
    database: Database
    user: User
    password: Pass

```

#### Uso desde un pipeline

```python
db_mssql = CORE.DATABASE.factory.get_database(
    connection_name="operational_db",
    env="prod",
    pipeline=self.pipeline
)

engine_mssql = db_mssql.start_connection()
```

Parámetros:

- connection_name - Nombre lógico definido en el YAML
- env - Entorno de ejecución (dev / qa / prod)
- pipeline - Nombre del pipeline para integración con logging

El driver y las credenciales se resuelven automáticamente a partir del archivo de configuración correspondiente al entorno.

#### Motores soportados

Actualmente el Core soporta los siguientes motores:

**Microsoft SQL Server (MSSQL)**

Motor relacional empresarial ampliamente utilizado en entornos corporativos y hospitalarios.

Tecnología utilizada:

- SQLAlchemy
- pyodbc
- Driver ODBC configurable desde YAML

Características:

- Conexión mediante mssql+pyodbc
- Uso de cadena ODBC construida dinámicamente
- Soporte para TrustServerCertificate
- Driver configurable (ej: ODBC Driver 17 for SQL Server)

Ejemplo de configuración YAML:

```yaml
connections:
  operational_db:
    engine: mssql
    driver: ODBC Driver 17 for SQL Server
    host: 192.168.1.10
    port: 1433
    database: Database
    user: user
    password: password
```

Casos típicos de uso:

- Sistemas transaccionales
- HIS / ERP hospitalarios
- Bases de datos on-premise
- Data extraction para procesos ETL

**MySQL**

Motor relacional ampliamente usado en aplicaciones web y sistemas operacionales livianos.

Tecnología utilizada:

- SQLAlchemy
- PyMySQL (driver configurable desde YAML)

Características:

- Conexión mediante mysql+pymysql
- Driver definido desde configuración
- Compatible con servidores locales y remotos
- Soporte para múltiples conexiones en el mismo pipeline

Ejemplo de configuración YAML:

```yaml
connections:
  analytics_db:
    engine: mysql
    driver: pymysql
    host: localhost
    port: 3306
    database: analytics
    user: user
    password: password
```

Casos típicos de uso:

- Bases de datos analíticas
- Aplicaciones web
- Sistemas intermedios
- Staging areas para procesos ETL

## 8 Buenas prácticas

- No hardcodear credenciales
- No modificar el Core desde un pipeline
- Versionar correctamente antes de cambios mayores

## 9 Versionado

Se recomienda Semantic Versioning:

**MAJOR.MINOR.PATCH**

Ejemplo:

- 0.1.0 → versión inicial
- 0.2.0 → nuevas funcionalidades
- 0.2.1 → bugfix

## 10 Novedades — Versión 2.0.0

La versión **2.0.0** introduce una evolución significativa del DATA-PIPELINE-CORE, transformándolo desde un conjunto de utilidades compartidas hacia un **mini framework estandarizado para pipelines de datos**.

Esta versión incorpora capacidades de observabilidad, estandarización estructural y reutilización avanzada de componentes.

---

### 10.1 Nuevo módulo DBLOG

Se incorpora el módulo **DBLOG**, diseñado para persistir en base de datos el historial de ejecución de los pipelines.

Objetivos principales:

- Registrar ejecuciones de pipelines
- Mantener trazabilidad histórica
- Facilitar auditoría operativa
- Permitir futuras métricas y dashboards de ejecución

Capacidades:

- Registro de inicio y fin de ejecución
- Estados de ejecución (SUCCESS, FAILED)
- Integración directa con el sistema de logging
- Preparado para monitoreo centralizado

Esto permite evolucionar hacia observabilidad operacional del ecosistema de datos.


---

### 10.2 Estandarización mediante `main_pipeline`

Se introduce el módulo:

**CORE.PIPELINES.main_pipeline**


El cual define una estructura base reutilizable para la construcción de pipelines.

Objetivos:

- Reducir código repetitivo
- Estandarizar el flujo de ejecución
- Centralizar el seguimiento del pipeline
- Facilitar mantenimiento y escalabilidad

Responsabilidades:

- Inicialización del logger
- Manejo del ciclo de vida del pipeline
- Control de etapas (stages)
- Integración con DBLOG
- Punto único de ejecución

Beneficio principal:

Los nuevos pipelines requieren menor código boilerplate y mantienen comportamiento homogéneo.

Estructura de las tablas para el log:

Se debe ejecutar sobre las bases de datos dev y prod los siguientes scripts los cuales crearan las tablas para el manejo del log:

```sql
CREATE TABLE `LogPipeline` (
  `Id` bigint PRIMARY KEY AUTO_INCREMENT,
  `Pipel` varchar(500) NOT NULL,
  `PipeV` varchar(50) NOT NULL,
  `CoreV` varchar(50) NOT NULL,
  `FchReg` datetime NOT NULL,
  `Est` bool DEFAULT false
);

CREATE TABLE `Logpipeline1` (
  `Id` bigint,
  `Cons` int,
  `ScriptName` varchar(500),
  `Est` bool DEFAULT false,
  `Obsv` varchar(5000),
  PRIMARY KEY (`Id`, `Cons`)
);

ALTER TABLE `Logpipeline1` ADD FOREIGN KEY (`Id`) REFERENCES `LogPipeline` (`Id`);

GRANT INSERT,SELECT,UPDATE ON `LogPipeline` TO 'user'@'%';
GRANT INSERT,SELECT,UPDATE ON `Logpipeline1` TO 'user'@'%';
```

---

### 10.3 Mejora en `PipelineLoggerAdapter`

Se actualiza el manejo del contexto del logger para soportar correctamente campos dinámicos mediante `extra`.

Nuevo comportamiento:

- Soporte nativo para `stage`
- Inyección automática de metadata del pipeline
- Compatibilidad con logging estructurado

Ejemplo:

```python
self.logger.info(
    "Inicio del pipeline",
    extra={"stage": "START"}
)
```

Salida:

```txt
2026-03-02 | INFO | hospitalizacion | START | Inicio del pipeline
```

Esto permite seguimiento granular por etapas.

---

### 10.4 Ajustes en estrategia `FullRefresh`

Se mejora la lógica de procesos Full Refresh, permitiendo:

- Ejecuciones más controladas
- Separación clara entre staging y fact tables
- Mayor reutilización dentro de utilities
- Mejor integración con logging y métricas

Estos cambios preparan el Core para soportar múltiples estrategias de carga futuras.

---

### 10.5 Nueva utilidad: Loader de Queries

Se introduce la utilidad Loader, diseñada para cargar archivos dinámicamente desde una estructura estándar de proyecto

Funcionalidad:

Permite cargar cualquier archivo (principalmente SQL) enviando únicamente:

- path raíz del pipeline
- nombre del archivo

Estructura esperada:

```txt
pipeline/
 └── queries/
      └── extract.sql
```

Uso conceptual:

```python
self.loader = loader(logger,dir)
query = self.loader.load_query(query_name="name query")
```

Beneficios:

- Eliminación de rutas hardcodeadas
- Portabilidad entre pipelines
- Convención única de organización
- Reutilización automática

---

### 10.6 Utilities reutilizables ampliadas

El Core amplía la capa de utilities para operaciones comunes entre pipelines, incluyendo:

- Carga dinámica de archivos
- Integración directa con logging
- Las utilities ahora forman parte del flujo estándar del framework.

---

### 10.7 Enfoque arquitectónico de la versión 2.0.0

La evolución del Core introduce tres pilares:

- Estandarización
- Pipeline base reutilizable
- Observabilidad
- Logging estructurado
- Registro en base de datos
- Reutilización
- Utilities desacopladas
- Loader dinámico

Esto posiciona al DATA-PIPELINE-CORE como una base para una futura plataforma interna de datos.

---

### 10.8 Cambios incompatibles (Breaking Changes)

- Se recomienda que nuevos pipelines utilicen main_pipeline.
- El manejo manual del logger queda desaconsejado fuera del Core.
- Las nuevas utilities asumen estructura estándar de carpetas.

### 10.9 Migración recomendada

Para actualizar pipelines existentes:

- Actualizar versión del Core.
- Migrar inicialización hacia main_pipeline.
- Reemplazar cargas manuales de SQL por Loader.
- Adoptar stages en logging.

## 11 Autor

![green-divider](https://user-images.githubusercontent.com/7065401/52071924-c003ad80-2562-11e9-8297-1c6595f8a7ff.png)

**Diego Ortiz Puerto**  
Data analyst / Data Engineer / developer
orpudi1001@gmail.com  
Colombia

![green-divider](https://user-images.githubusercontent.com/7065401/52071924-c003ad80-2562-11e9-8297-1c6595f8a7ff.png)
