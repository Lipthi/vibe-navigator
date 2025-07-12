import { useState } from 'react';
import './App.css';

function App() {
  const [city, setCity] = useState('');
  const [category, setCategory] = useState('');
  const [preference, setPreference] = useState('');
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchVibe = async () => {
    setError('');
    if (!query && (!city || !category || !preference)) {
      setError('Please fill in city, category, and preference or use a natural query.');
      return;
    }

    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (query) params.append("query", query);
      else {
        params.append("city", city);
        params.append("category", category);
        params.append("preference", preference);
      }

      const res = await fetch(`https://vibe-navigator-xbpj.onrender.com/summarize?${params.toString()}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError('Error fetching vibe summary');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">🌆 Vibe Navigator</h1>

      <div className="form">
        <input placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} className="input" />
        <input placeholder="Category (e.g., cafe)" value={category} onChange={(e) => setCategory(e.target.value)} className="input" />
        <input placeholder="Your Preference (e.g., solo, cozy)" value={preference} onChange={(e) => setPreference(e.target.value)} className="input" />
        <input placeholder="Or enter a full natural query (optional)" value={query} onChange={(e) => setQuery(e.target.value)} className="input" />

        <button className="c-button c-button--gooey" onClick={fetchVibe}>
          Get Vibe
          <span className="c-button__blobs"><span></span><span></span><span></span></span>
        </button>
        <svg style={{ display: 'none' }}>
          <filter id="goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
            <feColorMatrix in="blur" mode="matrix"
              values="1 0 0 0 0  
                      0 1 0 0 0  
                      0 0 1 0 0  
                      0 0 0 20 -10" result="goo" />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </svg>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p className="loading">⏳ Fetching vibe summary...</p>}

      {result && !loading && (
        <div className="card">
          <h2>{result.emojis} Vibe Summary</h2>
          <p>{result.vibe}</p>

          {result.places?.length > 0 && (
            <>
              <h3>Recommended Places:</h3>
              <ol>
                {result.places.map((place, i) => (
                  <li key={i}>{place}</li>
                ))}
              </ol>
            </>
          )}

          <p><strong>Tags:</strong></p>
          <div className="card-tags">
            {result.tags.map((tag, i) => (
              <span key={i} className="tag-chip">{tag}</span>
            ))}
          </div>

          {result.citations.length > 0 && (
            <>
              <h3>Citations:</h3>
              <ul>
                {result.citations.slice(0, 5).map((url, i) => (
                  <li key={i}><a href={url} target="_blank" rel="noopener noreferrer">{url}</a></li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
