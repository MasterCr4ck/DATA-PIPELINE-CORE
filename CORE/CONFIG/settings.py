from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[2] / "CORE" / "CONFIG"

def load_database_config(env: str):
    path = BASE_DIR / f"database.{env}.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Environment config not found: {env}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_connection_config(connection_name: str, env: str):
    db_config = load_database_config(env)

    try:
        return db_config["connections"][connection_name]
    except KeyError:
        raise ValueError(
            f"Connection '{connection_name}' not found in '{env}' environment"
        )
