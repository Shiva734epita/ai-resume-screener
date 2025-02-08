"use client";

import { useEffect, useState } from "react";

export function useFetchUser() {
  const [user, setUser] = useState<{ full_name: string; email: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem("token") ?? "";
      if (!token) return;

      try {
        const response = await fetch("http://localhost:5006/api/user-details", {
          method: "GET",
          headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        });

        const data = await response.json();
        if (response.ok) {
          setUser({ full_name: data.full_name, email: data.email });
        } else {
          setError(data.message || "Failed to fetch user data.");
        }
      } catch {
        setError("Error fetching user data.");
      }
    };

    fetchUserData().finally(() => setLoading(false));
  }, []);

  return { user, error, loading };
}
