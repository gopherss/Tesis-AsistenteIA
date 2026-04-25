import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
}

const Input = ({ label, ...rest }: InputProps) => {
    return (
        <div className='w-full'>
            {label && (
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    {label}
                </label>
            )}
            <input
                {...rest}
                className="      w-full h-11
          px-4
          border border-gray-300
          rounded-lg
          focus:ring-2 focus:ring-indigo-500
          focus:border-transparent
          outline-none
          transition-all"
            />
        </div>
    );
};

export default Input;
