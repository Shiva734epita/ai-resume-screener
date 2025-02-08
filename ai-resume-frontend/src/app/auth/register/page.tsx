"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import GlobalLayout from "@/components/ui/GlobalLayout";
import InputField from "@/components/ui/InputField";
import { useRouter } from "next/navigation";
import Navbar from "@/components/ui/Navbar";

export default function RegisterPage() {
  const [formData, setFormData] = useState({ email: "", password: "", name: "", otp: "" });
  const [otpSent, setOtpSent] = useState(false);
  const [otpValidated, setOtpValidated] = useState(false);
  const [error, setError] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [mounted, setMounted] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div suppressHydrationWarning={true}></div>;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.name]: e.target.type === "checkbox" ? (e.target as HTMLInputElement).checked : e.target.value,
    }));
  };

  const handleOtpRequest = async () => {
    if (!formData.name || !formData.email || !formData.password) {
      setError("All fields are required.");
      return;
    }

    if (!agreed) {
      setError("You must agree to the terms to continue.");
      return;
    }

    setError("");

    try {
      const response = await fetch("http://localhost:5006/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          name: formData.name,
          legal_details: { terms_accepted: agreed, privacy_policy: true },
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Failed to send OTP");
      } else {
        setOtpSent(true);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  const handleOtpValidation = async () => {
    setError("");

    try {
      const response = await fetch("http://localhost:5006/api/validate-registration-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.email,
          otp: formData.otp,
          password: formData.password,
          name: formData.name,
          legal_details: { terms_accepted: agreed, privacy_policy: true },
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Invalid OTP");
      } else {
        setOtpValidated(true);
        router.push("/auth/login");
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <GlobalLayout>
      <Navbar showLogin={true} showHome={true} />
      <div className="flex justify-center items-center w-full min-h-screen">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative w-full max-w-md p-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg shadow-lg rounded-lg border border-gray-300 dark:border-gray-700"
        >
          <h2 className="text-2xl font-semibold text-center text-gray-900 dark:text-white mb-6">Sign Up</h2>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          <form className="space-y-4">
            <InputField type="text" name="name" placeholder="Full Name" onChange={handleChange} />
            <InputField type="email" name="email" placeholder="Email" onChange={handleChange} />
            <InputField type="password" name="password" placeholder="Password" onChange={handleChange} />

            <label className="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300">
              <input type="checkbox" onChange={(e) => setAgreed(e.target.checked)} className="w-4 h-4" />
              <span>
                I agree to the{" "}
                <Link href="/terms" className="text-blue-600 dark:text-blue-300 hover:underline">
                  Terms & Conditions
                </Link>
              </span>
            </label>

            {!otpSent ? (
              <button
                type="button"
                className={`w-full py-3 ${
                  agreed ? "bg-blue-600 hover:bg-blue-700" : "bg-gray-500"
                } text-white font-semibold rounded-lg shadow-md transition-all`}
                onClick={handleOtpRequest}
                disabled={!agreed}
              >
                Get OTP
              </button>
            ) : (
              <>
                <InputField type="text" name="otp" placeholder="Enter OTP" onChange={handleChange} />
                {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

                {!otpValidated ? (
                  <button
                    type="button"
                    className="w-full py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition-all"
                    onClick={handleOtpValidation}
                  >
                    Validate OTP
                  </button>
                ) : (
                  <Link href="/auth/login">
                    <button className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-all">
                      Register
                    </button>
                  </Link>
                )}
              </>
            )}
          </form>

          <p className="mt-4 text-center text-sm text-gray-700 dark:text-gray-300">
            Already have an account?{" "}
            <Link href="/auth/login" className="text-blue-600 dark:text-blue-300 hover:underline">
              Login
            </Link>
          </p>
        </motion.div>
      </div>
    </GlobalLayout>
  );
}
