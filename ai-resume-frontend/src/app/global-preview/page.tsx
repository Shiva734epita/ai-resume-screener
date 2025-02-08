import GlobalLayout from "@/components/ui/GlobalLayout";

export default function GlobalPreview() {
  return (
    <GlobalLayout>
      <div className="text-center p-10">
        <h1 className="text-4xl font-bold text-white">🌍 Global Layout Preview</h1>
        <p className="text-lg text-gray-300 mt-4">
          This page shows how the global layout is applied across all pages. 
        </p>
      </div>
    </GlobalLayout>
  );
}
