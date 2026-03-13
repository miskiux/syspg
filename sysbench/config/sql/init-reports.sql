CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    test_name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    threads INTEGER,
    tps_rate NUMERIC,
    p95_latency_ms NUMERIC,
    env_details JSONB,
    db_settings JSONB
);