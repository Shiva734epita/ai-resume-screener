"use client";

import { useRouter } from "next/navigation";

type UserProfileProps = {
  fullName: string;
  email: string;
  onLogout: () => void;
};

export default function UserProfile({ fullName, email, onLogout }: UserProfileProps) {
  const router = useRouter();

  return (
    <div className="flex justify-between items-center w-full px-6 py-4 bg-gray-900 rounded-lg">
      <div>
        <h1 className="text-xl font-bold text-white">Welcome to Your Dashboard</h1>
        <p className="text-gray-400">Manage your resumes and explore AI-powered job assistance.</p>
        <p className="text-white mt-2"><strong>{fullName}</strong> ({email})</p>
      </div>
      <button
        onClick={onLogout}
        className="px-4 py-2 bg-red-500 text-white rounded-lg shadow-md hover:bg-red-600 transition"
        aria-label="Logout"
      >
        Logout
      </button>
    </div>
  );
}
