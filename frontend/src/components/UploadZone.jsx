import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import apiClient from '../utils/api';

export default function UploadZone({ threshold, onConversionComplete }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const selectedFile = acceptedFiles[0];
    if (selectedFile) {
      setFile(selectedFile);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(selectedFile);

      // Clear previous status
      setStatus(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.bmp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setStatus(null);
  };

  const handleConvert = async () => {
    if (!file) return;

    setLoading(true);
    setStatus(null);

    try {
      const result = await apiClient.convertImage(file, threshold);

      setStatus({
        type: 'success',
        message: 'Conversion successful! Check history below.',
      });

      // Notify parent to refresh history
      if (onConversionComplete) {
        onConversionComplete();
      }

      // Clear file after successful conversion
      setTimeout(() => {
        clearFile();
      }, 2000);

    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Conversion failed';
      setStatus({
        type: 'error',
        message: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Upload Image</h2>

      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-primary bg-blue-50' : 'border-gray-300 bg-gray-50 hover:border-primary hover:bg-gray-100'}`}
      >
        <input {...getInputProps()} />

        {!file ? (
          <>
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="mt-2 text-sm text-gray-600">
              {isDragActive ? 'Drop the image here...' : 'Drag & drop an image here, or click to browse'}
            </p>
            <p className="mt-1 text-xs text-gray-500">
              Supports: JPG, PNG, BMP (Max 10MB)
            </p>
          </>
        ) : (
          <>
            <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded" />
            <p className="mt-2 text-sm font-medium">{file.name}</p>
            <button
              onClick={(e) => {
                e.stopPropagation();
                clearFile();
              }}
              className="mt-2 text-danger text-sm hover:underline"
            >
              Remove
            </button>
          </>
        )}
      </div>

      {/* Convert Button */}
      <button
        onClick={handleConvert}
        disabled={!file || loading}
        className="w-full mt-4 bg-primary hover:bg-primary-dark text-white font-semibold py-3 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Converting...' : 'Convert to DXF'}
      </button>

      {/* Status Message */}
      {status && (
        <div
          className={`mt-4 p-3 rounded ${
            status.type === 'success'
              ? 'bg-green-50 text-green-800'
              : 'bg-red-50 text-red-800'
          }`}
        >
          {status.message}
        </div>
      )}
    </div>
  );
}
