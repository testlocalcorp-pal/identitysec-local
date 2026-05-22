"""
Flink job: aggregates login/auth events into 1-minute windows for the
fraud/risk pipeline. Reads from Kafka topic `events.login_attempted`,
writes to `agg.login_attempts_1m`.
"""
from pyflink.datastream import StreamExecutionEnvironment


def build_job():
    env = StreamExecutionEnvironment.get_execution_environment()
    return env
