import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Marathi.css';

function Marathi() {
  const [quote, setQuote] = useState('');

  useEffect(() => {
    // Fetch the quote from the Flask server
    fetch('http://localhost:4000/mar_quotes')
      .then((response) => response.json())
      .then((data) => setQuote(data.quote))
      .catch((error) => console.error('Error fetching quote:', error));
  }, []);

  const navigate = useNavigate();
  function handleClick(event) {
  navigate('/');
  }

  return (
    <div className="back">
      <div class="box">
        <h2>Quote of the day</h2>
        <blockquote>{quote}</blockquote>
        <button class="button-29" role="button" onClick={handleClick}>Regenerate</button>
      </div>
    </div>
  );
}

export default Marathi;