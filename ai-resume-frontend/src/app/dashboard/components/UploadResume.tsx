"use client";

type UploadResumeProps = {
  onUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  uploading: boolean;
};

export default function UploadResume({ onUpload, uploading }: UploadResumeProps) {
  return (
    <div className="w-full h-[50vh] bg-gray-100 dark:bg-gray-900 p-4 rounded-lg shadow-md transition-colors flex flex-col items-center justify-center">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white text-center">📤 Upload Your Resume</h2>
      <p className="text-gray-600 dark:text-gray-400 text-sm mb-2 text-center">
        Upload your resume to analyze and receive AI-powered feedback.
      </p>

      <label className="cursor-pointer bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg shadow-md transition-all flex items-center justify-center relative">
        <span>Upload Resume</span>
        <input
          type="file"
          className="absolute opacity-0 w-0 h-0"
          onChange={onUpload}
          accept=".pdf,.doc,.docx"
          aria-label="Upload your resume file (PDF or DOC)"
        />
      </label>

      {uploading && (
        <p className="text-yellow-500 dark:text-yellow-400 mt-2 text-center">Uploading...</p>
      )}
    </div>
  );
}
