export default function ConversionSettings({ threshold, setThreshold }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Settings</h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Threshold: {threshold}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={threshold}
            onChange={(e) => setThreshold(parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>More Detail</span>
            <span>Less Detail</span>
          </div>
        </div>

        <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
          <strong>Tip:</strong> Start with 50%. Increase for cleaner lines, decrease for more detail.
        </div>
      </div>
    </div>
  );
}
