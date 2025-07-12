import React from "react";

const VibeResult = ({ result }) => {
  if (!result) return null;

  return (
    <div className="vibe-result">
      <h2>Vibe Summary ✨</h2>
      <p>{result.vibe}</p>

      <h3>Tags:</h3>
      <ul>
        {result.tags.map((tag, idx) => (
          <li key={idx}>#{tag}</li>
        ))}
      </ul>

      <h3>Emojis:</h3>
      <p>{result.emojis}</p>

      <h3>Reddit Sources:</h3>
      <ul>
        {result.citations.map((link, idx) => (
          <li key={idx}>
            <a href={link} target="_blank" rel="noreferrer">
              Source {idx + 1}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VibeResult;
