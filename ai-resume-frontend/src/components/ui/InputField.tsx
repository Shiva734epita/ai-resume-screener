"use client";

export default function InputField({
  type,
  name,
  placeholder,
  onChange
}: {
  type: string;
  name: string;
  placeholder: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}) {
  return (
    <input
      type={type}
      name={name}
      placeholder={placeholder}
      onChange={onChange}
      className="w-full px-4 py-3 border border-gray-300 rounded-md dark:bg-gray-900 dark:border-gray-700 dark:text-white 
                 focus:outline-none focus:ring-2 focus:ring-blue-600 dark:focus:ring-blue-400 transition-all shadow-sm"
      required
    />
  );
}
