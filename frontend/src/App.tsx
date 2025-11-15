import { useState, useEffect, useMemo } from 'react';
import './App.css';
import SentimentPieChart from './components/SentimentPieChart';
import VolumeChart from './components/VolumeChart'; // Import the new VolumeChart

// Define the TypeScript types for our data
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

function App() {
  const [mentions, setMentions] = useState<Mention[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // useEffect hook to fetch data when the component loads
  useEffect(() => {
    const fetchMentions = async () => {
      try {
        setLoading(true);
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const response = await fetch(`${API_URL}/api/dashboard-mentions`);        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log("DATA FROM BACKEND:", data.mentions); // For debugging sentiment
        setMentions(data.mentions);
      } catch (error) {
        console.error("Failed to fetch mentions:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMentions();
  }, []);

  // Calculate sentiment counts. useMemo prevents recalculating on every render.
  const sentimentCounts = useMemo(() => {
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
        {/* New dashboard grid layout */}
        <div className="dashboard-grid">
          {/* Sentiment Chart Section */}
          <div className="dashboard-card chart-container">
            <SentimentPieChart data={sentimentCounts} />
          </div>

          {/* Volume Chart Section */}
          <div className="dashboard-card chart-container">
            <VolumeChart mentions={mentions} />
          </div>
          
          {/* Mentions Feed Section - Spans across both columns */}
          <div className="dashboard-card mentions-feed full-width">
            <h2>Latest Mentions</h2>
            {loading ? (
              <p>Loading mentions...</p>
            ) : mentions.length === 0 ? (
              <p>No mentions found. Try fetching some data for a brand!</p>
            ) : (
              <ul>
                {mentions.map((mention) => (
                  <li key={mention._id} className="mention-card">
                    <div className="mention-header">
                      <span className="source-name">{mention.source_name}</span>
                      {mention.sentiment && (
                        <span className={`sentiment-badge sentiment-${mention.sentiment.label.toLowerCase()}`}>
                          {mention.sentiment.label}
                        </span>
                      )}
                    </div>
                    <h3><a href={mention.url} target="_blank" rel="noopener noreferrer">{mention.title}</a></h3>
                    <p>{mention.text}</p>
                    <span className="publish-date">
                      {new Date(mention.published_at).toLocaleString()}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;