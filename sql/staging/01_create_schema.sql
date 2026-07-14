CREATE TABLE network_traffic (
    id SERIAL PRIMARY KEY,
    destination_port INT,
    flow_duration BIGINT,
    total_fwd_packets BIGINT,
    total_bwd_packets BIGINT,
    total_length_fwd_packets BIGINT,
    total_length_bwd_packets BIGINT,
    flow_bytes_per_sec FLOAT,
    flow_packets_per_sec FLOAT,
    label VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);