import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

base_dir = Path(__file__).resolve().parent

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


@dataclass    
class BenchmarkConfig:
    profile: str = ""
    script: str = ""
    settings: dict[str, any] = field(default_factory=dict)

    @classmethod
    def load(cls):
        profile = os.getenv("BENCHMARK_PROFILE")
        filepath = base_dir / f"{profile}.yaml"       

        if filepath.exists():
            with open(filepath, "r") as f:
                raw = yaml.safe_load(f)

            return cls(
            profile=raw.get("profile"),
            script=raw.get("script"),
            settings=raw.get("settings"),
        )
        
        raise FileNotFoundError(filepath)

