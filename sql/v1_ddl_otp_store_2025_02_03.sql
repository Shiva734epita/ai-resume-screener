-- Drop the table if it already exists
DROP TABLE IF EXISTS otp_store;

-- Create the otp_store table with improved structure
CREATE TABLE otp_store (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    otp VARCHAR(6) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Ensure changes are committed
COMMIT;