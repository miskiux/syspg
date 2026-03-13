import argparse
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from params import Params
from env import db_host, db_name, db_password, db_user
from context import Context, bootstrap_context


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

        self.flags = [
            # infrastructure (env)
            f"--pgsql-host={db_host}",
            f"--pgsql-user={db_user}",
            f"--pgsql-password={db_password}",
            f"--pgsql-db={db_name}",
            "--db-driver=pgsql",
            # test tuning (params volume with defaults)
            f"--threads={p.get(t, 'threads', '8')}",
            f"--tables={p.get(t, 'tables', '1')}",
            f"--table-size={p.get(t, 'table_size', '10000')}",
            f"--time={p.get(t, 'time', '60')}",
            f"--report-interval={p.get(t, 'report_interval', '1')}",
        ]

    def execute(self, command: Command) -> str:
        """
        Executes a sysbench command as a subprocess.
        """
        cmd = ["sysbench"] + self.flags + [self.test_name, command.value]
        self.log.info(f"sysbench command - {command.value}. test suite - {self.test_name}")
        
        try:
            subprocess.run(
                cmd,
                text=True, 
                check=True
            )
        except subprocess.CalledProcessError as e:
            self.log.error(f"sysbench command - {command.value} failed. error - {e.stderr.strip()}")
            raise

    @abstractmethod
    def run_task(self):
        """
        Defines the execution policy for a specific benchmark lifecycle.
        
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
            exit(1)