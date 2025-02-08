/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class", // ✅ Ensures dark mode works via class toggling
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/context/**/*.{js,ts,jsx,tsx}", // ✅ Ensures theme context is included
    "./src/app/globals.css",
    "./node_modules/@shadcn/ui/dist/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2563EB", // ✅ Custom primary color (optional)
        secondary: "#1E293B", // ✅ Custom secondary color (optional)
      },
    },
  },
  plugins: [require("@tailwindcss/forms")], // ✅ Ensures consistent form styling
};
