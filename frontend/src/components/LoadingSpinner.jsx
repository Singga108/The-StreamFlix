import React from 'react';

const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div 
        className={`${sizeClasses[size]} border-4 border-gray-600 border-t-red-500 rounded-full animate-spin`}
      ></div>
    </div>
  );
};

export const ContentLoader = ({ message = "Loading content..." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <LoadingSpinner size="lg" />
      <p className="text-gray-400 mt-4">{message}</p>
    </div>
  );
};

export const InlineLoader = ({ message = "Loading..." }) => {
  return (
    <div className="flex items-center justify-center space-x-2 py-8">
      <LoadingSpinner size="sm" />
      <span className="text-gray-400">{message}</span>
    </div>
  );
};

export default LoadingSpinner;