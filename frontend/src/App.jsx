import { useState } from 'react';
import UploadZone from './components/UploadZone';
import ConversionSettings from './components/ConversionSettings';
import HistoryList from './components/HistoryList';

function App() {
  const [threshold, setThreshold] = useState(50);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleConversionComplete = () => {
    // Trigger history refresh by changing the refreshTrigger value
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">DXF Converter Pro</h1>
          <p className="text-sm text-gray-600 mt-1">
            Convert images to DXF files for CNC plasma cutting
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Left Column - Upload & Settings */}
          <div className="lg:col-span-2 space-y-6">
            <UploadZone
              threshold={threshold}
              onConversionComplete={handleConversionComplete}
            />
            <ConversionSettings threshold={threshold} setThreshold={setThreshold} />
          </div>

          {/* Right Column - History */}
          <div className="lg:col-span-3">
            <HistoryList refreshTrigger={refreshTrigger} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="container mx-auto px-6 py-4 text-center text-sm text-gray-600">
          <p>DXF Converter Pro - Offline CNC Conversion Tool</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
