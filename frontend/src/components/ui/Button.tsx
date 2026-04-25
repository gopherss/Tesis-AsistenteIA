import type { ButtonHTMLAttributes } from "react";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  color: "primary" | "secondary" | "danger";
  full?: boolean;
}

const Button = ({
  label,
  color,
  full = false,
  ...props
}: Props) => {
  const variantStyles = {
    primary: "bg-indigo-600 hover:bg-indigo-700 text-white",
    secondary: "bg-gray-200 hover:bg-gray-300 text-gray-800",
    danger: "bg-red-600 hover:bg-red-700 text-white",
  };

  return (
    <button
      {...props}
      className={`
        px-4 py-2 rounded-lg
        focus:ring-2 focus:ring-indigo-500
        disabled:bg-gray-400 disabled:cursor-not-allowed
        transition-all whitespace-nowrap
        ${full ? "w-full" : ""}
        ${variantStyles[color]}
      `}
    >
      {label}
    </button>
  );
};

export default Button;