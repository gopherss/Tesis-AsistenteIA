import React from "react";
import { ChevronDown } from "lucide-react";

interface SelectOption {
  value: string | number;
  label: string;
}

interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  placeholder?: string;
}

const Select = ({
  label,
  options,
  placeholder = "Seleccione una opción",
  className = "",
  ...rest
}: SelectProps) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}

      <div className="relative">
        <select
          {...rest}
          className={`
            w-full h-11
            px-4 pr-10
            border border-gray-300
            rounded-lg
            bg-white
            text-gray-800
            appearance-none
            outline-none
            transition-all
            focus:ring-2 focus:ring-indigo-500
            focus:border-transparent
            disabled:bg-gray-100
            disabled:text-gray-400
            disabled:cursor-not-allowed
            ${className}
          `}
        >
          <option value="">{placeholder}</option>

          {options.map((item) => (
            <option
              key={item.value}
              value={item.value}
            >
              {item.label}
            </option>
          ))}
        </select>

        <ChevronDown
          size={18}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
        />
      </div>
    </div>
  );
};

export default Select;