import React from 'react';
import { Loader2 } from 'lucide-react';

/**
 * LoadingSpinner - Componente de carga reutilizable
 *
 * @param {string} size - Tamaño: 'sm', 'md', 'lg' (default: 'md')
 * @param {string} text - Texto a mostrar (opcional)
 * @param {boolean} fullScreen - Si es true, ocupa toda la pantalla (default: false)
 */
const LoadingSpinner = ({ size = 'md', text, fullScreen = false }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16',
  };

  const spinnerSize = sizes[size] || sizes.md;

  const content = (
    <div className="flex flex-col items-center justify-center">
      <Loader2 className={`${spinnerSize} text-blue-600 animate-spin`} />
      {text && (
        <p className="mt-3 text-sm text-gray-600 font-medium">{text}</p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
        {content}
      </div>
    );
  }

  return content;
};

export default LoadingSpinner;
