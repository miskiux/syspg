import json
import os
import re
from datetime import datetime

from base import BaseSysbench, Command
from env import db_name


class Run(BaseSysbench):
    def run_task(self):
        output_dir = "./stdout"
        file_name = (
            f"{self.test_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )
        output_path = os.path.join(output_dir, file_name)

        try:
            stdout = self.execute(Command.Run)
            stats = self.collect_stats(stdout)

            os.makedirs(output_dir, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump({**stats}, f, indent=4, default=str)

            self.log.info(
                "output_path:%s",
                output_path,
            )

        except Exception as e:
            self.log.error(e)

    def collect_stats(self, stdout):
        storage_usage = self.ctx.db.query("SELECT pg_size_pretty(pg_database_size(%s))", (db_name,)).fetchall()
        pg_ss = self.ctx.db.query("""
                SELECT 
                    query, 
                    calls, 
                    rows, 
                    shared_blks_hit, 
                    shared_blks_read,
                    mean_exec_time,
                    stddev_exec_time
                FROM pg_stat_statements 
                ORDER BY total_exec_time DESC 
                LIMIT 20;
            """).fetchall()

        sysb_metrics = {
            "tps_count": self.match(r"transactions:\s+(\d+)", stdout),
            "tps_rate": self.match(r"transactions:.*?\((\d+\.\d+) per sec\.\)", stdout),
            "qps_count": self.match(r"queries:\s+(\d+)", stdout),
            "qps_rate": self.match(r"queries:.*?\((\d+\.\d+) per sec\.\)", stdout),
            "errors_count": self.match(r"ignored errors:\s+(\d+)", stdout),
            "errors_rate": self.match(
                r"ignored errors:.*?\((\d+\.\d+) per sec\.\)", stdout
            ),
            "reconnects_count": self.match(r"reconnects:\s+(\d+)", stdout),
            "reconnects_rate": self.match(
                r"reconnects:.*?\((\d+\.\d+) per sec\.\)", stdout
            ),
            "avg_lat": self.match(r"avg:\s+(\d+\.\d+)", stdout),
            "p95_lat": self.match(r"95th percentile:\s+(\d+\.\d+)", stdout),
            "max_lat": self.match(r"max:\s+(\d+\.\d+)", stdout),
            "min_lat": self.match(r"min:\s+(\d+\.\d+)", stdout),
            "sum_lat": self.match(r"sum:\s+(\d+\.\d+)", stdout),
            "total_events": self.match(r"total number of events:\s+(\d+)", stdout),
            "read": self.match(r"read:\s+(\d+)", stdout),
            "write": self.match(r"write:\s+(\d+)", stdout),
            "other": self.match(r"other:\s+(\d+)", stdout),
            "events_avg": self.match(r"events \(avg/stddev\):\s+(\d+\.\d+)", stdout),
            "events_stddev": self.match(
                r"events \(avg/stddev\):.*?/(\d+\.\d+)", stdout
            ),
            "execution_avg": self.match(
                r"execution time \(avg/stddev\):\s+(\d+\.\d+)", stdout
            ),
            "execution_stddev": self.match(
                r"execution time \(avg/stddev\):.*?/(\d+\.\d+)", stdout
            ),
        }

        return {
            "storage_usage": storage_usage,
            "metadata": {**self.meta},
            "sysb_metrics": sysb_metrics,
            "pg_ss": pg_ss,
            "execution_log": stdout,
        }

    def match(self, pattern, content):
        match = re.search(pattern, content)
        if match:
            try:
                val = match.group(1)
                return float(val) if "." in val else int(val)
            except ValueError:
                return 0
        return 0


if __name__ == "__main__":
    Run.main()
