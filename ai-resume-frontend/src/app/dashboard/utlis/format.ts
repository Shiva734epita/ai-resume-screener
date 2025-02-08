export function formatSkills(skills: any): string {
    if (!skills) return "No skills listed";
    if (Array.isArray(skills)) {
      return skills.join(", ");
    }
    if (typeof skills === "object") {
      return Object.values(skills).flat().join(", ");
    }
    return "No skills listed";
  }
  
  export function formatDate(dateString: string | null | undefined): string {
    if (!dateString) return "Invalid date";
    const date = new Date(dateString);
    return isNaN(date.getTime()) ? "Invalid date" : date.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  }
