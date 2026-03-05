import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


base_dir = Path(__file__).resolve().parent

BENCHMARKS = {
    "db": "oltp_read_write"
}

@dataclass    
class BenchmarkConfig:
    test_name = BENCHMARKS.get(os.getenv("TEST_SUITE"))
    settings: dict[str, any] = field(default_factory=dict)

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    @classmethod
    def load(cls):
        filepath = base_dir / f"{cls.test_name}.yaml"       

        if filepath.exists():
            with open(filepath, "r") as f:
                raw = yaml.safe_load(f)

            return cls(
            cls.test_name,
            settings=raw.get("settings"),
        )
        
        raise FileNotFoundError(filepath)

