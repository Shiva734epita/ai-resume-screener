import React from "react";

export default function FutureFeatures() {
  return (
    <div className="w-full mt-10 p-6 bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white rounded-lg shadow-lg text-center transition-colors">
      <h2 className="text-2xl font-bold mb-4">🚀 What's Coming Next?</h2>
      <p className="text-gray-700 dark:text-gray-300 mb-6">
        We're constantly innovating! Stay tuned for upcoming features that will
        revolutionize your job search experience. 🔥
      </p>

      <div className="flex flex-wrap justify-center gap-4 mt-4">
        {[
          "AI Job Matching",
          "Resume Enhancement",
          "Competitor Analysis",
          "LinkedIn Optimization",
          "AI Interview Prep",
        ].map((feature) => (
          <button
            key={feature}
            className="px-6 py-3 bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-lg cursor-not-allowed transition-all"
            aria-disabled="true"
          >
            {feature} (Soon)
          </button>
        ))}
      </div>
    </div>
  );
}
