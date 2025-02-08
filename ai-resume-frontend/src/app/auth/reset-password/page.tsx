"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import GlobalLayout from "@/components/ui/GlobalLayout";
import InputField from "@/components/ui/InputField";
import Navbar from "@/components/ui/Navbar";

export default function ResetPasswordPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div suppressHydrationWarning={true}></div>;

  const handleSendOtp = async () => {
    setError("");

    try {
      const response = await fetch("http://localhost:5006/api/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Failed to send OTP");
      } else {
        setOtpSent(true);
        router.push(`/auth/reset-password/verify?email=${email}`);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <GlobalLayout>
      <Navbar showLogin={true} showRegister={true} showHome={true} />
      <div className="flex justify-center items-center w-full min-h-screen">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative w-full max-w-md p-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg shadow-lg rounded-lg border border-gray-300 dark:border-gray-700"
        >
          <h2 className="text-2xl font-semibold text-center text-gray-900 dark:text-white mb-6">Reset Password</h2>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          <form className="space-y-4">
            <InputField
              type="email"
              name="email"
              placeholder="Enter your email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <button
              type="button"
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-all"
              onClick={handleSendOtp}
            >
              Get OTP
            </button>
          </form>

          {/* Back to Login */}
          <p className="mt-4 text-center text-sm text-gray-700 dark:text-gray-300">
            Remember your password?{" "}
            <Link href="/auth/login" className="text-blue-600 dark:text-blue-300 hover:underline">
              Back to Login
            </Link>
          </p>
        </motion.div>
      </div>
    </GlobalLayout>
  );
}
