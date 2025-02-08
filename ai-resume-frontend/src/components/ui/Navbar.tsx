"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import ThemeToggle from "./ThemeToggle";

interface NavbarProps {
  showLogin?: boolean;
  showRegister?: boolean;
  showHome?: boolean;
  showLogout?: boolean; // ✅ Added logout button visibility control
}

export default function Navbar({ showLogin = false, showRegister = false, showHome = false, showLogout = false }: NavbarProps) {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/auth/login");
  };

  return (
    <header className="fixed top-0 w-full bg-gray-100 dark:bg-gray-900 shadow-md p-4 flex justify-between items-center z-50 backdrop-blur-lg transition-all duration-500">
      {/* ✅ Left Section: Title + Theme Toggle */}
      <div className="flex items-center space-x-4">
        <Link href="/">
          <h1 className="text-2xl font-extrabold text-gray-900 dark:text-white cursor-pointer">
            AI Resume Screener
          </h1>
        </Link>
        <ThemeToggle /> {/* ✅ Theme Toggle Positioned Next to Title */}
      </div>

      {/* ✅ Right Section: Conditional Buttons */}
      <div className="flex gap-4">
        {Boolean(showHome) && (
          <Link href="/">
            <button className="px-4 py-2 rounded-md font-semibold border border-gray-500 text-gray-900 hover:bg-gray-100 
            dark:text-white dark:border-gray-400 dark:hover:bg-gray-800 transition">
              Home
            </button>
          </Link>
        )}

        {Boolean(showLogin) && (
          <Link href="/auth/login">
            <button className="px-4 py-2 rounded-md font-semibold border border-gray-500 text-gray-900 hover:bg-gray-100 
            dark:text-white dark:border-gray-400 dark:hover:bg-gray-800 transition">
              Login
            </button>
          </Link>
        )}

        {Boolean(showRegister) && (
          <Link href="/auth/register">
            <button className="px-4 py-2 rounded-md font-semibold bg-blue-600 text-white hover:bg-blue-700 transition">
              Get Started
            </button>
          </Link>
        )}

        {Boolean(showLogout) && (
          <button 
            onClick={handleLogout} 
            className="px-4 py-2 rounded-md font-semibold bg-red-600 text-white hover:bg-red-700 transition"
          >
            Logout
          </button>
        )}
      </div>
    </header>
  );
}
