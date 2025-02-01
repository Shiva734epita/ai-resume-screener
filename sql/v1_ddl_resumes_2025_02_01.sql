-- Drop the table if it already exists
DROP TABLE IF EXISTS resumes;

-- Create the resumes table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(512) NOT NULL,
    extracted_text TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ensure changes are committed
COMMIT;

