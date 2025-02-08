-- Drop table if it already exists
DROP TABLE IF EXISTS resumes;

-- Create resumes table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(512) NOT NULL,
    extracted_text TEXT NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    skills JSONB,  -- ✅ Optimized for PostgreSQL JSONB indexing
    job_role VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- ✅ Indexes for optimized search performance
CREATE INDEX idx_email ON resumes(email);         -- Fast lookups by email
CREATE INDEX idx_job_role ON resumes(job_role);   -- Faster job filtering
CREATE INDEX idx_user_id ON resumes(user_id);     -- Optimize query performance for user resumes
CREATE INDEX idx_uploaded_at ON resumes(uploaded_at);  -- Sorting optimization
