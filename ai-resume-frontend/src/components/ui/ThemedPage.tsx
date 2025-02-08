"use client";

import { motion } from "framer-motion";

export default function ThemedPage({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen transition-colors 
        bg-gradient-to-br from-[#F5F5F5] to-[#EAEAEA] 
        dark:from-[#121212] dark:to-[#1E1E1E] 
        text-gray-900 dark:text-white">
      
      {/* Animated Page Fade-in Effect */}
      <motion.div 
        initial={{ opacity: 0 }} 
        animate={{ opacity: 1 }} 
        transition={{ duration: 0.8 }}
        className="flex flex-col items-center w-full"
      >
        {children}
      </motion.div>
    </div>
  );
}
