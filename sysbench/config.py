import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

base_dir = Path(__file__).resolve().parent

@dataclass    
class BenchmarkConfig:
    workload: str = ""
    settings: dict[str, any] = field(default_factory=dict)

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    @classmethod
    def load(cls):
        test_suite = os.getenv("TEST_SUITE")
        filepath = base_dir / f"{test_suite}.yaml"       

        if filepath.exists():
            with open(filepath, "r") as f:
                raw = yaml.safe_load(f)

            workload = raw.get("test_alias") or raw.get("script")

            return cls(
            workload=workload,
            settings=raw.get("settings"),
        )
        
        raise FileNotFoundError(filepath)

