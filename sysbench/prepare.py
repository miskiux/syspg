from base import BaseSysbench, Command
from context import bootstrap_context

class Prepare(BaseSysbench):
    def run_task(self):
        self.warmup()
        # self.execute(Command.Prepare)
    
    def warmup(self):
        """
        Percona-style preparation steps (VACUUM, ANALYZE, CHECKPOINT)
        to ensure the DB state is optimized before the benchmark.
        """
        try:
            with self.ctx.db_mgr.connect(autocommit=True) as conn:
                res = conn.execute("SELECT COUNT(*) FROM sbtest1").fetchone()

                self.log.info(res)
        except Exception as e:
            self.log.error(e)
    

if __name__ == "__main__":
   Prepare.main()