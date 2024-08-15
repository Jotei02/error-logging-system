CREATE TABLE error_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    error_trace TEXT,
    url TEXT,
    method TEXT,
    user_agent TEXT,
    status_code INTEGER
);
