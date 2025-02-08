"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import GlobalLayout from "@/components/ui/GlobalLayout";
import InputField from "@/components/ui/InputField";
import Navbar from "@/components/ui/Navbar";

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({ email: "", password: "", otp: "" });
  const [otpSent, setOtpSent] = useState(false);
  const [error, setError] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div suppressHydrationWarning={true}></div>;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendOtp = async () => {
    setError("");

    try {
      const response = await fetch("http://localhost:5006/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: formData.email, password: formData.password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Failed to send OTP");
      } else {
        setOtpSent(true);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
      console.error("Error:", err);
    }
  };

  const handleVerifyOtp = async () => {
    setError("");

    try {
      const response = await fetch("http://localhost:5006/api/validate-login-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: formData.email, otp: formData.otp }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Invalid OTP");
      } else {
        if (data.token) {
          localStorage.removeItem("token");
          localStorage.setItem("token", data.token);

          // Decode token and store user_id
          const decodedToken = JSON.parse(atob(data.token.split(".")[1]));
          localStorage.setItem("user_id", decodedToken.user_id);

          window.location.href = "/dashboard";
        } else {
          setError("Login failed: No token received");
        }
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
      console.error("Error:", err);
    }
  };

  return (
    <GlobalLayout>
      <Navbar showRegister={true} showHome={true} />
      <div className="flex flex-col items-center justify-center text-center px-6 pt-[6rem] pb-20">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative w-full max-w-md p-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg shadow-lg rounded-lg border border-gray-300 dark:border-gray-700"
        >
          <h2 className="text-2xl font-semibold text-center text-gray-900 dark:text-white mb-6">Login</h2>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          <form className="space-y-4">
            <InputField type="email" name="email" placeholder="Email" onChange={handleChange} />
            <InputField type="password" name="password" placeholder="Password" onChange={handleChange} />

            {!otpSent ? (
              <button
                type="button"
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all"
                onClick={handleSendOtp}
              >
                Login
              </button>
            ) : (
              <>
                <InputField type="text" name="otp" placeholder="Enter OTP" onChange={handleChange} />
                <button
                  type="button"
                  className="w-full py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition-all"
                  onClick={handleVerifyOtp}
                >
                  Verify OTP & Login
                </button>
              </>
            )}
          </form>

          <p className="mt-4 text-center text-sm text-gray-700 dark:text-gray-300">
            Don't have an account?{" "}
            <Link href="/auth/register" className="text-blue-600 dark:text-blue-300 hover:underline">
              Register
            </Link>
          </p>
          <p className="mt-2 text-center text-sm text-gray-700 dark:text-gray-300">
            <Link href="/auth/reset-password" className="text-blue-600 dark:text-blue-300 hover:underline">
              Forgot Password?
            </Link>
          </p>
        </motion.div>
      </div>
    </GlobalLayout>
  );
}
