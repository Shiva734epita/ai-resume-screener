-- Drop the table if it already exists
DROP TABLE IF EXISTS resumes;

-- Create the resumes table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(512) NOT NULL,
    extracted_text TEXT NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    skills TEXT,
    job_role VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Ensure changes are committed
COMMIT;

SELECT * FROM resumes;

