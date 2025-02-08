// src/app/dashboard/hooks/useTokenExpirationHandler.ts
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";

interface JwtPayload {
  exp: number; // expiration time in seconds
}

export function useTokenExpirationHandler(onRefresh: () => Promise<boolean>) {
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) return;

    try {
      const decoded = jwtDecode<JwtPayload>(token);
      const expTime = decoded.exp * 1000; // convert seconds to milliseconds
      const currentTime = Date.now();
      const timeLeft = expTime - currentTime;

      // Set a timer to prompt the user 1 minute before token expiry
      if (timeLeft > 60000) {
        const timer = setTimeout(() => {
          setShowModal(true);
        }, timeLeft - 60000);
        return () => clearTimeout(timer);
      } else {
        // If less than 1 minute remains, show the modal immediately.
        setShowModal(true);
      }
    } catch (error) {
      console.error("Error decoding token:", error);
    }
  }, []);

  // Call this when the user confirms to continue the session
  const handleContinue = async () => {
    setShowModal(false);
    await onRefresh();
  };

  return { showModal, handleContinue, setShowModal };
}
