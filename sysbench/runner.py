from dataclasses import asdict
import logging
import subprocess
from enum import Enum
from config import BenchmarkConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Command(str, Enum):
    PREPARE = "prepare"
    RUN = "run"
    CLEANUP = "cleanup"
    HELP = "help"

class SysbenchRunner:
    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.flags = [
            f"--pgsql-host={config.db_host}",
            f"--pgsql-user={config.db_user}",
            f"--pgsql-password={config.db_password}",
            f"--pgsql-db={config.db_name}",
            "--db-driver=pgsql",
        ]

        for key, value in self.config.settings.items():
            flag_name = key.replace("_", "-")
            self.flags.append(f"--{flag_name}={value}")

    def _execute(self, command: Command):
        cmd = ["sysbench"]  + self.flags + [self.config.test_name, command.value]

        logging.info(f"sysbench_cmd: {cmd}")
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing {command}: {e.stderr}")
            raise


    def warmup(self):
        print("SEED DATA")
        self._execute(Command.PREPARE)
        print("VACUUM ANALYZED")

    def run(self):
        self.warmup()
        self._execute(Command.RUN)

    def cleanup():
        print('CLEANUP')


if __name__ == "__main__":
  try:
    config = BenchmarkConfig.load()
    logging.info(f"starting_benchmark: {config}")

    runner = SysbenchRunner(config)
    logging.info("sysbench_runner_started")
    runner.run()
    logging.info("benchmark_complete")
  except Exception as e:
    logging.error(f"benchmark_failed: {e}", exc_info=True)
