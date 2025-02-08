"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import GlobalLayout from "@/components/ui/GlobalLayout";
import InputField from "@/components/ui/InputField";
import Navbar from "@/components/ui/Navbar";

export default function VerifyResetPasswordPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get("email") || "";

  const [formData, setFormData] = useState({ otp: "", newPassword: "", confirmPassword: "" });
  const [error, setError] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (!email) {
      router.push("/auth/reset-password");
    }
  }, [email, router]);

  if (!mounted) return <div suppressHydrationWarning={true}></div>;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleResetPassword = async () => {
    setError("");

    if (formData.newPassword !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5006/api/update-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp: formData.otp, new_password: formData.newPassword }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Failed to reset password");
      } else {
        router.push("/auth/login");
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <GlobalLayout>
      <Navbar />
      <div className="flex justify-center items-center w-full min-h-screen">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative w-full max-w-md p-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg shadow-lg rounded-lg border border-gray-300 dark:border-gray-700"
        >
          <h2 className="text-2xl font-semibold text-center text-gray-900 dark:text-white mb-6">
            Verify OTP & Reset Password
          </h2>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          <form className="space-y-4">
            <InputField type="text" name="otp" placeholder="Enter OTP" onChange={handleChange} />
            <InputField type="password" name="newPassword" placeholder="New Password" onChange={handleChange} />
            <InputField type="password" name="confirmPassword" placeholder="Confirm Password" onChange={handleChange} />

            <button
              type="button"
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-all"
              onClick={handleResetPassword}
            >
              Reset Password
            </button>
          </form>

          {/* Back to Reset Password */}
          <p className="mt-4 text-center text-sm text-gray-700 dark:text-gray-300">
            Didn’t receive an OTP?{" "}
            <Link href="/auth/reset-password" className="text-blue-600 dark:text-blue-300 hover:underline">
              Resend OTP
            </Link>
          </p>
        </motion.div>
      </div>
    </GlobalLayout>
  );
}
