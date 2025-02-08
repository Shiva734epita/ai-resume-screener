"use client";

import { useEffect, useState } from "react";
import { useTheme } from "@/context/ThemeContext";
import { motion } from "framer-motion";
import Link from "next/link";
import GlobalLayout from "@/components/ui/GlobalLayout";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/ui/Navbar";

export default function LandingPage() {
  const { theme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div suppressHydrationWarning={true}></div>;

  return (
    <GlobalLayout>
      <Navbar showHome={true} />
      {/* Hero Section */}
      <main className="flex flex-col items-center justify-center text-center px-6 pt-[6rem] pb-20">
        <motion.h2 
          className="text-6xl font-extrabold mb-6 text-gray-900 dark:text-white drop-shadow-lg"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          AI-Powered Resume Optimization
        </motion.h2>

        <motion.p 
          className="text-lg text-gray-800 dark:text-gray-300 max-w-3xl drop-shadow-md"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          Transform your resume with AI insights and get noticed by recruiters.  
          Get real-time feedback, job match scores, and ensure your resume beats the ATS!
        </motion.p>

        <motion.div 
          className="mt-8 flex space-x-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
        >
          <Link href="/auth/login">
          <motion.button
            className="px-6 py-3 text-lg bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-lg transition-transform duration-300 hover:scale-105"
          >
            Upload Resume
          </motion.button>
          </Link>
          <Link href="/auth/register">
            <Button variant="outline" className="px-6 py-3 text-lg text-gray-900 dark:text-white border-gray-900 dark:border-white hover:bg-gray-900 hover:text-white dark:hover:bg-white dark:hover:text-gray-900 transition">
              Get Started
            </Button>
          </Link>
        </motion.div>

        {/* AI Illustration */}
        <motion.div
          className="mt-12 w-full max-w-lg"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.9, duration: 1 }}
        >
          <img src="/ai-illustration.svg" alt="AI Resume Optimization" className="w-full" />
        </motion.div>
      </main>

      {/* Features Section */}
      <section className="py-16 px-6 text-center">
        <h3 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white drop-shadow-lg">Why Choose Us?</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { title: "AI Resume Scoring", desc: "Receive AI-driven feedback to refine your resume." },
            { title: "Job Match Analysis", desc: "Find jobs that align perfectly with your skills." },
            { title: "ATS Optimization", desc: "Ensure your resume passes applicant tracking systems." },
          ].map((feature, index) => (
            <motion.div 
              key={index}
              className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-lg p-6 rounded-lg shadow-lg border border-gray-300 dark:border-gray-600"
              whileHover={{ scale: 1.05 }}
            >
              <h4 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{feature.title}</h4>
              <p className="text-gray-700 dark:text-gray-300">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </GlobalLayout>
  );
}