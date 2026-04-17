from pathlib import Path

class Params:
    def __init__(self, base_path="config/params"):
        self.base_path = Path(base_path)

    def get(self, test_name: str, key: str, default=None):
        path = self.base_path / test_name / key
        if path.exists():
            return path.read_text().strip()
        return default