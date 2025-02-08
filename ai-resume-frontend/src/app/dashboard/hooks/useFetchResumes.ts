"use client";

import { useEffect, useState } from "react";

// ✅ Define the Resume type
type Resume = {
  id: number;
  filename: string;
  filepath: string;
  name: string;
  email: string;
  phone: string;
  skills: string[];
  job_role: string;
  uploaded_at: string;
};


export function useFetchResumes() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResumes = async () => {
      const token = localStorage.getItem("token") ?? "";
      if (!token) return;

      try {
        const response = await fetch("http://localhost:5006/api/resumes", {
          method: "GET",
          headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        });

        const data = await response.json();
        if (response.ok) {
          setResumes(data.resumes);
        } else {
          setError(data.message || "No resumes found.");
        }
      } catch {
        setError("Error fetching resumes.");
      }
    };

    fetchResumes();
  }, []);

  return { resumes, setResumes, error };
}
