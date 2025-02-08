// src/app/dashboard/hooks/auth.ts
export async function refreshToken(): Promise<boolean> {
    const storedRefreshToken = localStorage.getItem("refreshToken");
    if (!storedRefreshToken) return false;
  
    try {
      const response = await fetch("http://localhost:5006/api/refresh-token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refreshToken: storedRefreshToken }),
      });
      const data = await response.json();
      if (response.ok && data.accessToken) {
        localStorage.setItem("accessToken", data.accessToken);
        // If the backend sends a new refresh token, update it too.
        if (data.refreshToken) {
          localStorage.setItem("refreshToken", data.refreshToken);
        }
        return true;
      } else {
        console.error("Failed to refresh token:", data.error);
        return false;
      }
    } catch (error) {
      console.error("Error refreshing token:", error);
      return false;
    }
  }
  