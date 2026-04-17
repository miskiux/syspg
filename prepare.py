import os
import subprocess

from base import BaseSysbench, Command


class Prepare(BaseSysbench):
    def run_task(self):
        try:
            self.seed()
            self.maintenance()
            self.prewarm()
            self.reset_stats()

        except Exception as e:
            raise e

    def seed(self):
        try:
            stdout = self.execute(Command.Prepare)
            self.log.info("seed_success: %s", stdout)
        except Exception:
            self.log.info("seed_failed: %s", stdout)

    def maintenance(self):
        """
        percona benchmark prep guidelines: CHECKPOINT, VACUUM ANALYZE.
        """
        workers = os.cpu_count() or 1
        cmd = ["vacuumdb", "-j", str(workers), "-z", "-v", "--dbname", self.ctx.db.dsn]

        try:
            self.ctx.db.query("CHECKPOINT")
            self.log.info("postgres_checkpoint: success")

            subprocess.run(cmd, check=True, capture_output=True, text=True)
    
        except subprocess.CalledProcessError as e:
            raise e

    def prewarm(self):
        result = self.ctx.db.query(
            "SELECT tablename FROM pg_tables WHERE tablename LIKE 'sbtest%'"
        ).fetchall()

        for row in result:
            self.ctx.db.query(f"SELECT pg_prewarm('{row['tablename']}')")

        self.log.info("prewarm_done: %d", len(result))

    def reset_stats(self):
        self.ctx.db.query("SELECT pg_stat_statements_reset()")
        self.ctx.db.query("SELECT pg_stat_monitor_reset()")


if __name__ == "__main__":
    Prepare.main()
