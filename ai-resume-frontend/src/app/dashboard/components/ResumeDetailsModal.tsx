"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

type Resume = {
  name: string;
  email: string;
  phone: string;
  skills: string[];
  job_role: string;
};

type ResumeDetailsModalProps = {
  isOpen: boolean;
  onClose: () => void;
  resume: Resume | null;
};

export function formatSkills(skills: any): string {
  if (!skills || typeof skills !== "object") return "No skills listed";

  // ✅ Flatten nested skill categories into a single array
  const extractedSkills = Object.values(skills).flat().filter((skill) => skill !== "");

  return extractedSkills.length > 0 ? extractedSkills.join(", ") : "No skills listed";
}

export default function ResumeDetailsModal({ isOpen, onClose, resume }: ResumeDetailsModalProps) {
  if (!resume) return null; // ✅ Prevents rendering without data

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1000] bg-white/90 dark:bg-gray-900/90 
                                text-gray-900 dark:text-white p-10 pt-20 pb-24 rounded-lg shadow-2xl w-[95%] max-w-2xl max-h-[90vh] overflow-y-auto transition-all">
        <DialogHeader className="absolute top-6 left-1/2 -translate-x-1/2 w-[90%] text-center">
            <div>
              <DialogTitle>📑 Resume Details</DialogTitle>
            </div>
          </DialogHeader>

          <div className="space-y-6 mt-8 max-h-[70vh] overflow-y-auto pr-2">
            <p><strong>Name:</strong> {resume.name}</p>
            <p><strong>Email:</strong> {resume.email}</p>
            <p><strong>Phone:</strong> {resume.phone}</p>
            <p><strong>Job Role:</strong> {resume.job_role}</p>
            <p><strong>Skills:</strong> {formatSkills(resume.skills)}</p>
            {/* {Array.isArray(resume.skills) ? resume.skills.join(", ") : "No skills listed"} */}
          </div>

          <div className="sticky bottom-0 left-0 w-full bg-white/90 dark:bg-gray-900/90 p-4 flex justify-center shadow-md">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-all" onClick={onClose}>
              Close
            </button>
          </div>
      </DialogContent>
    </Dialog>
  );
}

