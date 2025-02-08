-- Drop the table if it already exists
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW(),
    legal_details JSONB NOT NULL, -- Store legal details securely
);

-- Ensure changes are committed
COMMIT;


select * from users