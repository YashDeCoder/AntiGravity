import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, SlidersHorizontal, RefreshCw, PlusCircle, LayoutGrid, List as ListIcon } from 'lucide-react';
import Sidebar from './components/Sidebar';
import HousingCard from './components/HousingCard';

const App = () => {
  const [activeTab, setActiveTab] = useState('housing');
  const [houses, setHouses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);

  // Filters
  const [maxBudget, setMaxBudget] = useState(1250);
  const [maxDuration, setMaxDuration] = useState(30);
  const [selectedSource, setSelectedSource] = useState('all');
  const [showBuy, setShowBuy] = useState(false);
  const [address, setAddress] = useState('Hoekenrode 10A, 1101 DT Amsterdam');

  const fetchHouses = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/houses`, {
        params: {
          max_budget: maxBudget,
          max_duration: maxDuration > 0 ? maxDuration : null,
          source: selectedSource,
          show_buy: showBuy,
          address: address
        }
      });
      setHouses(response.data);
    } catch (error) {
      console.error("Error fetching houses:", error);
    } finally {
      setLoading(false);
    }
  };

  const startScrape = async () => {
    setScanning(true);
    try {
      await axios.post(`http://localhost:8000/scrape?city=amsterdam`);
      fetchHouses();
    } catch (error) {
      console.error("Error scraping:", error);
    } finally {
      setScanning(false);
    }
  };

  useEffect(() => {
    fetchHouses();
  }, [maxBudget, maxDuration, selectedSource, showBuy, address]);

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary flex">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="ml-64 flex-1 p-8">
        {activeTab === 'housing' && (
          <div className="max-w-7xl mx-auto flex flex-col gap-8">
            {/* Header */}
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <h1 className="text-4xl font-bold tracking-tight mb-2">Housing <span className="gradient-text">Hub</span></h1>
                <p className="text-text-secondary">Explore potential homes based on your budget and travel preferences.</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={startScrape}
                  disabled={scanning}
                  className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${scanning
                    ? 'bg-bg-secondary text-text-muted cursor-not-allowed'
                    : 'bg-glass text-text-primary border border-glass-border hover:bg-bg-tertiary'
                    }`}
                >
                  <RefreshCw size={20} className={scanning ? 'animate-spin' : ''} />
                  {scanning ? 'Scanning Sources...' : 'Refresh Listings'}
                </button>
                <button className="flex items-center gap-2 px-6 py-3 rounded-xl bg-accent-primary text-white font-semibold shadow-lg shadow-accent-primary/20 hover:bg-accent-secondary transition-all">
                  <PlusCircle size={20} />
                  Add Manual
                </button>
              </div>
            </header>

            {/* Filters Bar */}
            <div className="glass rounded-2xl p-6 flex flex-wrap items-center gap-8 border border-border-color">
              <div className="flex flex-col gap-2 min-w-[200px]">
                <label className="text-xs font-semibold uppercase tracking-widest text-text-muted flex items-center gap-2">
                  <SlidersHorizontal size={14} /> Max Budget
                </label>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="500"
                    max="5000"
                    step="100"
                    value={maxBudget}
                    onChange={(e) => setMaxBudget(Number(e.target.value))}
                    className="flex-1 h-1.5 bg-bg-tertiary rounded-lg appearance-none cursor-pointer accent-accent-primary"
                  />
                  <span className="text-sm font-medium w-16">€{maxBudget}</span>
                </div>
              </div>

              <div className="flex flex-col gap-2 min-w-[200px]">
                <label className="text-xs font-semibold uppercase tracking-widest text-text-muted flex items-center gap-2">
                  <RefreshCw size={14} /> Max Commute
                </label>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="5"
                    max="120"
                    step="5"
                    value={maxDuration}
                    onChange={(e) => setMaxDuration(Number(e.target.value))}
                    className="flex-1 h-1.5 bg-bg-tertiary rounded-lg appearance-none cursor-pointer accent-accent-secondary"
                  />
                  <span className="text-sm font-medium w-16">{maxDuration} min</span>
                </div>
              </div>
              <div className="flex flex-col gap-2 min-w-[150px]">
                <label className="text-xs font-semibold uppercase tracking-widest text-text-muted flex items-center gap-2">
                  <LayoutGrid size={14} /> Source
                </label>
                <select
                  value={selectedSource}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="bg-bg-tertiary text-text-primary text-sm rounded-lg border-none focus:ring-1 focus:ring-accent-primary p-2 cursor-pointer transition-all hover:bg-bg-secondary"
                >
                  <option value="all">All Sources</option>
                  <option value="Funda">Funda</option>
                  <option value="Verhuurtbeter">Verhuurtbeter</option>
                  <option value="Pararius">Pararius</option>
                </select>
              </div>

              <div className="flex flex-col gap-2 min-w-[150px]">
                <label className="text-xs font-semibold uppercase tracking-widest text-text-muted flex items-center gap-2">
                  <LayoutGrid size={14} /> Address
                </label>
                <input
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="bg-bg-tertiary text-text-primary text-sm rounded-lg border-none focus:ring-1 focus:ring-accent-primary p-2 cursor-pointer transition-all hover:bg-bg-secondary"
                />
              </div>

              <div className="flex flex-col gap-2 min-w-[150px]">
                <label className="text-xs font-semibold uppercase tracking-widest text-text-muted flex items-center gap-2">
                  <LayoutGrid size={14} /> Show Buy
                </label>
                <input
                  type="checkbox"
                  checked={showBuy}
                  onChange={(e) => setShowBuy(e.target.checked)}
                  className="bg-bg-tertiary text-text-primary text-sm rounded-lg border-none focus:ring-1 focus:ring-accent-primary p-2 cursor-pointer transition-all hover:bg-bg-secondary"
                />
              </div>

              <div className="flex-1" />

              <div className="flex items-center bg-bg-tertiary/50 p-1 rounded-xl border border-glass-border">
                <button className="p-2 rounded-lg bg-bg-primary text-accent-primary shadow-sm">
                  <LayoutGrid size={20} />
                </button>
                <button className="p-2 rounded-lg text-text-muted hover:text-text-primary">
                  <ListIcon size={20} />
                </button>
              </div>
            </div>

            {/* Content Grid */}
            {loading ? (
              <div className="flex flex-col items-center justify-center py-32 gap-4">
                <div className="w-12 h-12 border-4 border-accent-primary border-t-transparent rounded-full animate-spin" />
                <p className="text-text-secondary animate-pulse">Fetching premium listings...</p>
              </div>
            ) : houses.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {houses.map((house) => (
                  <HousingCard key={house._id} house={house} />
                ))}
              </div>
            ) : (
              <div className="text-center py-32 glass rounded-3xl border border-dashed border-border-color">
                <Search size={48} className="mx-auto text-text-muted mb-4 opacity-50" />
                <h3 className="text-xl font-semibold mb-2">No houses found</h3>
                <p className="text-text-secondary">Try adjusting your budget or commute filters.</p>
              </div>
            )}
          </div>
        )}

        {activeTab !== 'housing' && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h2 className="text-3xl font-bold mb-4 capitalize">{activeTab} Coming Soon</h2>
              <p className="text-text-secondary">We're currently focusing on the Housing Hub. Stay tuned!</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
