import os

def print_tree(startpath, prefix="", show_files=False):
    """ Recursively prints folder structure in a tree format, keeping only essential directories and key files """
    if not os.path.exists(startpath):
        print(f"❌ Path does not exist inside function: {startpath}")
        return  # Exit the function early

    # Define what to exclude
    exclude_dirs = {"venv", "node_modules", "__pycache__", ".git", "logs", "migrations", "dist", "build", ".idea",".next"}
    essential_files = {"config.py", "run.py", "README.md", "docker-compose.yml", "requirements.txt", "package.json"}

    items = sorted(os.listdir(startpath))
    
    # Filter directories and files
    filtered_items = [
        item for item in items 
        if (os.path.isdir(os.path.join(startpath, item)) and item not in exclude_dirs) 
        or (show_files and (item.endswith(".py") or item.endswith(".tsx") or item in essential_files))
    ]
    
    for index, name in enumerate(filtered_items):
        path = os.path.join(startpath, name)
        connector = "├── " if index < len(filtered_items) - 1 else "└── "
        print(prefix + connector + name)
        if os.path.isdir(path):  # If it's a directory, recurse
            new_prefix = prefix + ("│   " if index < len(filtered_items) - 1 else "    ")
            print_tree(path, new_prefix, show_files)

# ✅ Set absolute paths for backend & frontend
backend_path = "/Users/muralikrish/Documents/ai-resume-screener"
frontend_path = "/Users/muralikrish/Documents/ai-resume-screener/ai-resume-frontend"

# ✅ Run for Backend
print("📂 Backend Folder Structure:")
print_tree(backend_path, show_files=True)

print("\n📂 Frontend Folder Structure:")
print_tree(frontend_path, show_files=True)


# "use client";

# import { useEffect, useState } from "react";
# import { useRouter } from "next/navigation";
# import GlobalLayout from "@/components/ui/GlobalLayout";
# import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

# // ✅ Define Resume type
# type Resume = {
#   id: number;
#   filename: string;
#   filepath: string;
#   name: string;
#   email: string;
#   phone: string;
#   skills: string[];
#   job_role: string;
#   uploaded_at: string;
# };

# export default function Dashboard() {
#   const router = useRouter();
#   const [user, setUser] = useState<{ full_name: string; email: string }>({ full_name: "", email: "" });
#   const [loading, setLoading] = useState(true);
#   const [error, setError] = useState("");
#   const [resumes, setResumes] = useState<Resume[]>([]);
#   const [selectedResume, setSelectedResume] = useState<Resume | null>(null);
#   const [uploading, setUploading] = useState(false);
#   const [isModalOpen, setIsModalOpen] = useState(false);

#   // ✅ Fetch user details & resumes on page load
#   useEffect(() => {
#     const fetchUserData = async () => {
#       const token = localStorage.getItem("token") ?? "";

#       if (!token) {
#         router.push("/auth/login");
#         return;
#       }

#       try {
#         const userResponse = await fetch("http://localhost:5006/api/user-details", {
#           method: "GET",
#           headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
#         });

#         const userData = await userResponse.json();
#         if (userResponse.ok) {
#           setUser({ full_name: userData.full_name, email: userData.email });
#           fetchUserResumes(token);
#         } else {
#           setError(userData.message || "Failed to load user data");
#         }
#       } catch {
#         setError("Error fetching user data");
#       } finally {
#         setLoading(false);
#       }
#     };

#     fetchUserData();
#   }, []);

#   // ✅ Fetch user resumes
#   const fetchUserResumes = async (token: string) => {
#     try {
#       const response = await fetch("http://localhost:5006/api/resumes", {
#         method: "GET",
#         headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
#       });

#       const data = await response.json();
#       if (response.ok && data.resumes.length > 0) {
#         setResumes(data.resumes);
#       } else {
#         setResumes([]);
#       }
#     } catch {
#       setError("Error fetching resumes.");
#     }
#   };

#   // ✅ Handle resume upload
#   const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
#     const file = event.target.files?.[0];
#     if (!file) return;

#     setUploading(true);
#     const token = localStorage.getItem("token") ?? "";

#     const formData = new FormData();
#     formData.append("file", file);

#     try {
#       const response = await fetch("http://localhost:5006/api/upload-resume", {
#         method: "POST",
#         headers: { Authorization: `Bearer ${token}` },
#         body: formData,
#       });

#       const data = await response.json();
#       if (response.ok) {
#         setResumes([...resumes, { ...data.parsed_data, id: resumes.length + 1 }]);
#       } else {
#         alert(data.error || "Upload failed");
#       }
#     } catch {
#       alert("Error uploading resume");
#     } finally {
#       setUploading(false);
#     }
#   };

#   // ✅ Fetch resume details & show modal
#   const handleFetchResume = async (resumeId: number) => {
#     const token = localStorage.getItem("token") ?? "";

#     try {
#       const response = await fetch(`http://localhost:5006/api/resume/${resumeId}`, {
#         method: "GET",
#         headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
#       });

#       const data = await response.json();
#       if (response.ok) {
#         setSelectedResume(data);
#         setIsModalOpen(true);
#       } else {
#         alert(data.error || "Failed to fetch resume details");
#       }
#     } catch {
#       alert("Error fetching resume details.");
#     }
#   };

#   // ✅ Handle logout
#   const handleLogout = () => {
#     localStorage.removeItem("token");
#     router.push("/auth/login");
#   };

#   if (loading)
#     return (
#       <GlobalLayout>
#         <div className="flex justify-center items-center h-screen">
#           <p className="text-white text-lg">Loading...</p>
#         </div>
#       </GlobalLayout>
#     );

#   if (error)
#     return (
#       <GlobalLayout>
#         <div className="flex justify-center items-center h-screen">
#           <p className="text-red-500 text-lg">{error}</p>
#         </div>
#       </GlobalLayout>
#     );

#   return (
#     <GlobalLayout>
#       <div className="flex flex-col items-center justify-center min-h-screen space-y-6">
#         <h1 className="text-3xl font-bold text-white">Welcome, {user.full_name}!</h1>
#         <p className="text-lg text-gray-300">Your email: {user.email}</p>

#         {/* ✅ Upload Resume Button */}
#         <label className="cursor-pointer bg-blue-500 text-white px-5 py-3 rounded-lg shadow-md hover:bg-blue-600 transition">
#           Upload Resume
#           <input type="file" className="hidden" onChange={handleUpload} />
#         </label>

#         {uploading && <p className="text-yellow-400">Uploading...</p>}

#         {/* ✅ Display Uploaded Resumes */}
#         {resumes.length > 0 ? (
#           <div className="w-full max-w-2xl mt-6 p-4 bg-white/10 backdrop-blur-lg shadow-lg rounded-lg border border-white/30">
#             <h2 className="text-2xl font-semibold text-white">Your Resumes</h2>
#             <ul className="mt-4 space-y-2">
#               {resumes.map((resume) => (
#                 <li key={resume.id} className="flex justify-between items-center bg-white/10 p-3 rounded-lg shadow-md">
#                   <span className="text-white">{resume.filename}</span>
#                   <button
#                     className="px-4 py-2 bg-green-500 text-white rounded-lg shadow-md hover:bg-green-600 transition"
#                     onClick={() => handleFetchResume(resume.id)}
#                   >
#                     Get Details
#                   </button>
#                 </li>
#               ))}
#             </ul>
#           </div>
#         ) : (
#           <p className="text-gray-400 mt-6">No resumes found. Upload one to get started!</p>
#         )}

#         {/* ✅ Resume Details Modal */}
#         <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
#           <DialogContent className="fixed right-10 top-1/4 bg-gray-800 text-white p-6 rounded-lg shadow-lg w-96">
#             <DialogHeader>
#               <DialogTitle>Resume Details</DialogTitle>
#               <DialogDescription>View the details of your selected resume.</DialogDescription>
#             </DialogHeader>
#             {selectedResume && (
#               <div className="space-y-3">
#                 <p><strong>Name:</strong> {selectedResume.name}</p>
#                 <p><strong>Email:</strong> {selectedResume.email}</p>
#                 <p><strong>Phone:</strong> {selectedResume.phone}</p>
#                 <p><strong>Job Role:</strong> {selectedResume.job_role}</p>
#                 <p><strong>Skills:</strong> {
#                   Array.isArray(selectedResume.skills)
#                     ? selectedResume.skills.join(", ") 
#                     : typeof selectedResume.skills === "object" 
#                       ? Object.values(selectedResume.skills).flat().join(", ")
#                       : ""
#                 }</p>
#               </div>
#             )}
#             <button className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={() => setIsModalOpen(false)}>
#               OK
#             </button>
#           </DialogContent>
#         </Dialog>

#         <button onClick={handleLogout} className="mt-6 px-6 py-3 bg-red-500 text-white rounded-lg shadow-md hover:bg-red-600 transition">
#           Logout
#         </button>
#       </div>
#     </GlobalLayout>
#   );
# }
