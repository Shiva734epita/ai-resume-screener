import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/solid'; // Correct import of icons
import React, { useState } from 'react';

type Resume = {
  id: number;
  filename: string;
};

type ResumeListProps = {
  resumes: Resume[];
  onFetchDetails: (resumeId: number) => void;
  onDelete: (resumeId: number) => void;  // Callback to delete a resume
};

export default function ResumeList({ resumes, onFetchDetails, onDelete }: ResumeListProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleList = () => setIsExpanded((prev) => !prev);

  return (
    <div
      className={`w-full h-[50vh] bg-gray-100 dark:bg-gray-900 p-4 rounded-lg shadow-md transition-colors overflow-y-auto flex flex-col ${
        isExpanded ? '' : 'justify-center'
      }`}
    >
      {/* Header section */}
      <div className="flex justify-center items-center">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white text-center">
          📄 Your Uploaded Resumes
        </h2>
        <button
          onClick={toggleList}
          className="ml-4 px-2 py-1 text-sm bg-gray-300 dark:bg-gray-700 rounded-lg flex items-center"
          aria-label={isExpanded ? 'Collapse resume list' : 'Expand resume list'}
        >
          {isExpanded ? (
            <ChevronUpIcon className="w-5 h-5 text-gray-900 dark:text-white" />
          ) : (
            <ChevronDownIcon className="w-5 h-5 text-gray-900 dark:text-white" />
          )}
        </button>
      </div>

      {/* Conditional message */}
      <p className="text-gray-600 dark:text-gray-400 text-sm mb-2 text-center">
        {isExpanded
          ? 'Click "Get Details" to view resume details.'
          : 'Resume list is collapsed. Click "Expand" to view your uploaded resumes.'}
      </p>

      {/* Expanded list content */}
      {isExpanded && resumes.length > 0 && (
        <ul className="mt-4 space-y-2">
          {resumes.map((resume) => (
            <li
              key={resume.id}
              className="flex justify-between items-center bg-gray-200 dark:bg-gray-800 p-3 rounded-lg shadow-md transition-colors"
            >
              <span className="text-gray-900 dark:text-white">{resume.filename}</span>
              <div className="flex items-center space-x-2">
                <button
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow-md transition-all"
                  onClick={() => onFetchDetails(resume.id)}
                  aria-label={`Get details for ${resume.filename}`}
                >
                  Get Details
                </button>
                <button
                  className="px-2 py-2 bg-red-600 hover:bg-red-700 text-white rounded-full shadow-md transition-all"
                  onClick={() => onDelete(resume.id)}
                  aria-label={`Delete ${resume.filename}`}
                >
                  X
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {/* Message if expanded but no resumes */}
      {isExpanded && resumes.length === 0 && (
        <div className="text-gray-600 dark:text-gray-400 mt-6 text-center">
          <p>No resumes found. Start by uploading one!</p>
        </div>
      )}
    </div>
  );
}
