import os
import subprocess

from base import BaseSysbench, Command


class Prepare(BaseSysbench):
    def run_task(self):
        try:
            self.seed()
            self.maintenance()
            self.prewarm()
            self.ctx.db.query("SELECT pg_stat_statements_reset()")
        except Exception as e:
            self.log.error("Prepare task failed. Error: %s", e)
            raise

    def seed(self):
        try:
            stdout = self.execute(Command.Prepare)
            self.log.info("Seed complete. Results: %s", stdout)
        except Exception as e:
            self.log.error("Seed failed. Error: %s", e)

    def maintenance(self):
        """
        Percona benchmark prep guidelines: CHECKPOINT, VACUUM ANALYZE.
        """
        workers = os.cpu_count() or 1
        cmd = ["vacuumdb", "-j", str(workers), "-z", "-v", "--dbname", self.ctx.db.dsn]

        try:
            self.ctx.db.query("CHECKPOINT")
            self.log.info("Postgres CHECKPOINT issued successfully")

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.log.info("Vacuum output: %s", result.stdout)

        except subprocess.CalledProcessError as e:
            self.log.error(
                "Maintenance failed. Exit code: %s | Error: %s", e.returncode, e.stderr
            )
            raise

    def prewarm(self):
        result = self.ctx.db.query(
            "SELECT tablename FROM pg_tables WHERE tablename LIKE 'sbtest%'"
        ).fetchall()

        for row in result:
            self.ctx.db.query(f"SELECT pg_prewarm('{row['tablename']}')")

        self.log.info("Prewarm sequence for %s tables finished", len(result))


if __name__ == "__main__":
    Prepare.main()
