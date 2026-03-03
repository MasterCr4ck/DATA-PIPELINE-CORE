from dataclasses import dataclass
from datetime import datetime
from importlib.metadata import version

@dataclass
class BasePipelineMetadata:
    name: str
    version: str
    author: str
    description: str
    frequency: str
    created_at: datetime
    core_version: str = version("data-pipeline-core")
    
    def get_core_version(self) -> str:
        try:
            return version("data-pipeline-core")
        except Exception:
            return "unknown"

    def log_metadata(self, logger):
        logger.info(
            f"""
            ================= PIPELINE METADATA =================
            Name        : {self.name}
            Version     : {self.version}
            Author      : {self.author}
            Frequency   : {self.frequency}
            Created At  : {self.created_at}
            Description : {self.description}
            Core        : v{self.get_core_version()}
            ====================================================
            """
        )
    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "frequency": self.frequency,
            "created_at": self.created_at.isoformat()
        }