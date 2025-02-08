"use client";

import { useState, useEffect } from "react";
import UploadResume from "./components/UploadResume";
import ResumeList from "./components/ResumeList";
import ResumeDetailsModal from "./components/ResumeDetailsModal";
import FutureFeatures from "./components/FutureFeatures";
import { useFetchResumes } from "./hooks/useFetchResumes";
import GlobalLayout from "@/components/ui/GlobalLayout";
import Navbar from "@/components/ui/Navbar";

// >>> NEW: Import token refresh hook and refresh function
import { useTokenExpirationHandler } from "@/hooks/useTokenExpirationHandler";
import { refreshToken } from "@/hooks/auth";

export default function Dashboard() {
  const { resumes, setResumes } = useFetchResumes();
  const [selectedResume, setSelectedResume] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // >>> NEW: Initialize token expiration handler
  const { showModal, handleContinue, setShowModal } = useTokenExpirationHandler(refreshToken);

  useEffect(() => {
    if (selectedResume) {
      setIsModalOpen(true);
    }
  }, [selectedResume]);
  
  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
  
    setUploading(true);
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch("http://localhost:5006/api/upload-resume", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });
      const data = await response.json();
  
      if (response.ok) {
        alert("Resume uploaded successfully!");
        setTimeout(() => window.location.reload(), 500); // ✅ Reload page after upload
      } else {
        alert(data.error || "Upload failed");
      }
    } finally {
      setUploading(false);
    }
  };  

  const handleFetchResume = async (resumeId: number) => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(`http://localhost:5006/api/resume/${resumeId}`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      });
      const data = await response.json();
      console.log("DEBUG: Resume Data ->", data); // ✅ Check if data is received
  
      if (response.ok) {
        setSelectedResume(data);
        setIsModalOpen((prev) => !prev); // ✅ Forces state re-evaluation
        console.log("DEBUG: isModalOpen ->", isModalOpen); // ✅ Log if state updates
      }
    } catch (err) {
      console.error("Error fetching resume details:", err);
    }
  };  

  const handleDeleteResume = async (resumeId: number) => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch("http://localhost:5006/api/resume/delete", {
        method: "POST", // using POST as per your requirement
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ resume_id: resumeId })
      });
      const data = await response.json();
      if (response.ok && data.success) {
        // Remove the deleted resume from the state list
        setResumes(resumes.filter((r) => r.id !== resumeId));
        alert("Resume deleted successfully.");
      } else {
        alert(data.message || "Failed to delete resume.");
      }
    } catch (err) {
      console.error("Error deleting resume:", err);
      alert("An error occurred while deleting the resume.");
    }
  };

  return (
    <GlobalLayout>
      <Navbar showLogout={true} />
      <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white flex flex-col">

        {/* ✅ Upload & Resume List Side by Side */}
        <div className="flex flex-col md:flex-row gap-6 p-6">
          <div className="md:w-1/2">
            <UploadResume onUpload={handleUpload} uploading={uploading} />
          </div>
          <div className="md:w-1/2">
            <ResumeList resumes={resumes} 
                        onFetchDetails={handleFetchResume} 
                        onDelete={handleDeleteResume}/>
          </div>
        </div>

        {/* ✅ Resume Details (Expands Below) */}
        {selectedResume && (
          <ResumeDetailsModal 
            isOpen={isModalOpen} 
            onClose={() => { setIsModalOpen(false); setSelectedResume(null); }} 
            resume={selectedResume} 
          />
        )}

        {/* ✅ Future Features Section */}
        <FutureFeatures />

        {/* >>> NEW: Session Expiration Modal */}
        {showModal && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-lg">
              <h2 className="text-lg font-semibold mb-4">Session Expiring</h2>
              <p>Your session is about to expire. Would you like to continue?</p>
              <div className="mt-6 flex justify-end">
                <button
                  className="mr-2 px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  onClick={handleContinue}
                >
                  Continue
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </GlobalLayout>
  );
}
