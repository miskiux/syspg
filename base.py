import argparse
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
import time

from context import Context, bootstrap_context
from env import db_host, db_name, db_password, db_user
from params import Params


class Command(str, Enum):
    Prepare = "prepare"
    Run = "run"


class BaseSysbench(ABC):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.log = self.ctx.logger.getChild(self.__class__.__name__)

        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--test", dest="test_name", required=True)
        self.args = parser.parse_args()
        self.test_name = self.args.test_name

        self.params = Params()
        p = self.params
        t = self.test_name

        self.meta = {
            "test": t,
            "threads": p.get(t, "threads", "8"),
            "tables": p.get(t, "tables", "1"),
            "table-size": p.get(t, "table_size", "10000"),
            "time": p.get(t, "time", "60"),
            "report-interval": p.get(t, "report_interval", "1"),
        }

        self.flags = [
            f"--pgsql-host={db_host}",
            f"--pgsql-user={db_user}",
            f"--pgsql-password={db_password}",
            f"--pgsql-db={db_name}",
            "--db-driver=pgsql",
            f"--threads={self.meta['threads']}",
            f"--tables={self.meta['tables']}",
            f"--table-size={self.meta['table-size']}",
            f"--time={self.meta['time']}",
            f"--report-interval={self.meta['report-interval']}",
        ]

    def execute(self, command: Command) -> str:
        """
        Executes a sysbench command as a subprocess.
        """
        cmd = ["sysbench"] + self.flags + [self.test_name, command.value]
        self.log.info(
            "sysbench_progress: %s",
            {"status": "progress", **self.meta},
        )

        start = time.perf_counter()
        try:
            result = subprocess.run(cmd, text=True, check=True, capture_output=True)
            
            duration = round(time.perf_counter() - start, 3)
            self.log.info(
                "sysbench_complete: %s",
                {"status": "complete", "duration": duration,},
            )

            return result.stdout.strip()
        except subprocess.CalledProcessError:
            self.log.error(
                "test_err: %s",
                {"status": "error"},
            )

            raise

    @abstractmethod
    def run_task(self):
        """
        Concrete implementations must orchestrate the sequence of setup,
        sysbench actions, and database maintenance required for the task.
        """
        pass

    @classmethod
    def main(cls):
        try:
            ctx = bootstrap_context()

            app = cls(ctx)
            app.run_task()
        except Exception:
            import logging
            import sys
            import traceback

            logging.error(traceback.format_exc())
            sys.exit(1)
