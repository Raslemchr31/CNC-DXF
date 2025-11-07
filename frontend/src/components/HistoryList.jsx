import { useState, useEffect } from 'react';
import apiClient from '../utils/api';
import FileCard from './FileCard';

export default function HistoryList({ refreshTrigger }) {
  const [files, setFiles] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.getHistory(search);
      setFiles(response.data);
    } catch (err) {
      setError('Failed to load history');
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [search, refreshTrigger]);

  const handleDelete = () => {
    fetchHistory(); // Refresh list after delete
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Conversion History</h2>
        <span className="text-sm text-gray-500">{files.length} files</span>
      </div>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search files..."
        className="w-full px-4 py-2 border rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-primary"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12 text-gray-500">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="text-center py-12 text-red-500">
          <p>{error}</p>
          <button
            onClick={fetchHistory}
            className="mt-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark"
          >
            Retry
          </button>
        </div>
      )}

      {/* File List */}
      {!loading && !error && (
        <>
          {files.length > 0 ? (
            <div className="space-y-3 max-h-[600px] overflow-y-auto">
              {files.map((file) => (
                <FileCard key={file.id} file={file} onDelete={handleDelete} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <svg
                className="mx-auto h-12 w-12 text-gray-400 mb-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <p>No conversions yet</p>
              <p className="text-sm">Upload an image to get started</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
