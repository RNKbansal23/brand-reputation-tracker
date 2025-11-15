import { useState, useEffect, useMemo } from 'react';
import './App.css';
import SentimentPieChart from './components/SentimentPieChart';
import VolumeChart from './components/VolumeChart';

// Interfaces (no change)
interface Sentiment {
  label: 'Positive' | 'Negative' | 'Neutral' | 'Error' | 'Unknown';
  score: number;
}
interface Mention {
  _id: string;
  source_name: string;
  title: string;
  text: string;
  url: string;
  published_at: string;
  sentiment: Sentiment;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function App() {
  const [mentions, setMentions] = useState<Mention[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isFetching, setIsFetching] = useState<boolean>(false); // New state for loading indicator on buttons

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/dashboard-mentions`);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      setMentions(data.mentions);
    } catch (error) {
      console.error("Failed to fetch mentions:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // NEW FUNCTION TO TRIGGER THE BACKEND WORKER
  const handleFetchBrand = async (brandName: string) => {
    try {
      setIsFetching(true);
      alert(`Fetching new mentions for ${brandName}... The dashboard will refresh when complete.`);
      const response = await fetch(`${API_URL}/api/fetch-and-store/${brandName}`);
      if (!response.ok) throw new Error('Failed to fetch and store new mentions');
      const result = await response.json();
      console.log(result.message);
      // After fetching, refresh the dashboard data
      fetchDashboardData();
    } catch (error) {
      console.error(`Error fetching for ${brandName}:`, error);
      alert(`An error occurred while fetching data for ${brandName}.`);
    } finally {
      setIsFetching(false);
    }
  };

  const sentimentCounts = useMemo(() => { // (No change)
    return mentions.reduce(
      (acc, mention) => {
        if (!mention.sentiment || !mention.sentiment.label) return acc;
        const sentiment = mention.sentiment.label.toLowerCase();
        if (sentiment === 'positive') acc.positive++;
        else if (sentiment === 'negative') acc.negative++;
        else if (sentiment === 'neutral') acc.neutral++;
        return acc;
      },
      { positive: 0, negative: 0, neutral: 0 }
    );
  }, [mentions]);

  return (
    <div className="app-container">
      <header>
        <h1>Brand Reputation Tracker</h1>
      </header>
      <main>
        {/* NEW CONTROLS SECTION */}
        <div className="dashboard-card controls-container">
          <h3>Fetch New Mentions</h3>
          <p>Click a brand to fetch the latest articles. This may take a moment.</p>
          <div className="button-group">
            <button onClick={() => handleFetchBrand('Starbucks')} disabled={isFetching}>
              {isFetching ? 'Working...' : 'Fetch Starbucks'}
            </button>
            <button onClick={() => handleFetchBrand('NVIDIA')} disabled={isFetching}>
              {isFetching ? 'Working...' : 'Fetch NVIDIA'}
            </button>
            <button onClick={() => handleFetchBrand('Tesla')} disabled={isFetching}>
              {isFetching ? 'Working...' : 'Fetch Tesla'}
            </button>
          </div>
        </div>

        <div className="dashboard-grid">
          {/* (Rest of the JSX is the same) */}
          <div className="dashboard-card chart-container"><SentimentPieChart data={sentimentCounts} /></div>
          <div className="dashboard-card chart-container"><VolumeChart mentions={mentions} /></div>
          <div className="dashboard-card mentions-feed full-width">{/*...*/}</div>
        </div>
      </main>
    </div>
  );
}

export default App;