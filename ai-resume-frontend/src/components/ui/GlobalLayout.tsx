import React from "react";
import ThemedPage from "@/components/ui/ThemedPage";

export default function GlobalLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemedPage>
      <div className="relative w-full min-h-screen flex justify-center items-center
          bg-gradient-to-br from-[#F5F5F5] to-[#EAEAEA] dark:from-[#121212] dark:to-[#1E1E1E]
          transition-all duration-500 ease-in-out">
        
        <div className="absolute inset-0 bg-white/30 dark:bg-black/30 backdrop-blur-lg"></div> {/* Subtle Overlay */}
        <div className="relative z-10 w-full">{children}</div>
      </div>
    </ThemedPage>
  );
}
