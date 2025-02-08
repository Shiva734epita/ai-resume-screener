import React from "react";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "outline";
};

export const Button: React.FC<ButtonProps> = ({ variant = "primary", ...props }) => {
  return (
    <button
      {...props}
      className={`px-4 py-2 rounded-md font-semibold ${
        variant === "primary"
          ? "bg-blue-600 text-white hover:bg-blue-700"
          : "border border-gray-500 text-gray-900 hover:bg-gray-100 dark:text-white dark:border-gray-400 dark:hover:bg-gray-800"
      }`}
    />
  );
};
