import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

const Input = ({ label, error, ...rest }: InputProps) => {
    return (
        <div className='w-full'>
            {label && (
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    {label}
                </label>
            )}
            <input
                {...rest}
                className={`w-full h-11 px-4 border rounded-lg outline-none transition-all ${
                    error
                        ? 'border-red-400 focus:ring-2 focus:ring-red-500'
                        : 'border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent'
                }`}
            />
            {error && (
                <p className="text-red-500 text-xs mt-1">{error}</p>
            )}
        </div>
    );
};

export default Input;
