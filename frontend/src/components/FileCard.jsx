import { useState } from 'react';
import apiClient from '../utils/api';

export default function FileCard({ file, onDelete }) {
  const [loading, setLoading] = useState(false);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const handleDownload = async () => {
    setLoading(true);
    try {
      const blob = await apiClient.downloadDXF(file.id);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${file.filename}.dxf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download file');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this conversion?')) {
      return;
    }

    setLoading(true);
    try {
      await apiClient.deleteConversion(file.id);
      if (onDelete) {
        onDelete();
      }
    } catch (error) {
      console.error('Delete failed:', error);
      alert('Failed to delete file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-4 p-4 border rounded-lg hover:bg-gray-50 transition">
      {/* Thumbnail */}
      <div className="w-16 h-16 bg-gray-200 rounded flex-shrink-0 overflow-hidden">
        {file.thumbnail_url ? (
          <img
            src={apiClient.getThumbnailUrl(file.id)}
            alt={file.filename}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-gray-900 truncate">{file.filename}</h3>
        <div className="flex gap-4 text-sm text-gray-500 mt-1">
          <span>{formatDate(file.created_at)}</span>
          <span>{formatSize(file.file_size)}</span>
          <span>{file.metadata.total_entities || 0} entities</span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <button
          onClick={handleDownload}
          disabled={loading}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark disabled:opacity-50 transition-colors"
        >
          {loading ? '...' : 'Download'}
        </button>
        <button
          onClick={handleDelete}
          disabled={loading}
          className="px-4 py-2 text-danger hover:bg-red-50 rounded transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
