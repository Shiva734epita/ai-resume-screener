import type { Config } from "tailwindcss";

export default {
  darkMode: "class", // ✅ Ensures dark mode works via class toggling
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/context/**/*.{js,ts,jsx,tsx,mdx}", // ✅ Ensures ThemeContext.tsx is included
    "./src/app/globals.css",
    "./node_modules/@shadcn/ui/dist/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: "#2563EB", // ✅ Custom primary color (optional)
        secondary: "#1E293B", // ✅ Custom secondary color (optional)
      },
    },
  },
  plugins: [require("@tailwindcss/forms")], // ✅ Ensures consistent form styling
} satisfies Config;
