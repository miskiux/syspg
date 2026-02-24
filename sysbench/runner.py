from dataclasses import asdict
import subprocess

from sysbench.config import db_host, db_user, db_password, db_name, BenchmarkConfig 

class Command():
    PREPARE = "prepare"
    RUN = "run"
    CLEANUP = "cleanup"
    HELP = "help"

class SysbenchRunner:
    def __init__(self, config: BenchmarkConfig = BenchmarkConfig()):
        self.config = config

        self.flags = [
            f"--pgsql-host={db_host}",
            f"--pgsql-user={db_user}",
            f"--pgsql-password={db_password}",
            f"--pgsql-db={db_name}",
            "--db-driver=pgsql",
        ]

        for key, value in asdict(self.config.settings).items():
            flag_name = key.replace("_", "-")
            self.flags.append(f"--{flag_name}={value}")

    def _execute(self, command: Command):
        cmd = ["sysbench"] + [self.config.profile] + self.flags + [command.value]
        
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
  runner = SysbenchRunner()
  runner.run()
