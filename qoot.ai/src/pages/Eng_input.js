import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Eng_input.css';

function Eng_input() {
  const [seedText, setSeedText] = useState('');
  const [numWords, setNumWords] = useState(5);
  const [generatedQuote, setGeneratedQuote] = useState('');
  const [speaking, setSpeaking] = useState(false);

  const speakQuote = () => {
    const speechSynthesis = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(generatedQuote);
    speechSynthesis.speak(utterance);
  };

  const generateQuote = () => {
    const requestData = {
      seed_text: seedText,
      num_words: numWords,
    };

    fetch('http://localhost:5000/eng_quotes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        setGeneratedQuote(data.quote);
        setSpeaking(true); // Start speaking the quote
      })
      .catch((error) => {
        console.error('Error generating quote:', error);
      });
  };

  const navigate = useNavigate();

  function handleClick() {
    navigate('/');
  }

  useEffect(() => {
    if (speaking) {
      speakQuote();
      setSpeaking(false); // Stop speaking after speaking once
    }
  }, [speaking]);

  return (
    <div className="back">
      <div className="box">
        <div className="quote_div">
          <h2>Input to Generate Quotes</h2>
        </div>
        <div className="input_quote">
          <div>
            <label>
              Target Word{" "}
              <input
                type="text"
                value={seedText}
                onChange={(e) => setSeedText(e.target.value)}
              />
            </label>
          </div>

          <div>
            <label>
              Length of Quote{" "}
              <input
                type="number"
                value={numWords}
                onChange={(e) => setNumWords(e.target.value)}
              />
            </label>
          </div>
        </div>
        <button onClick={generateQuote}>Generate Quote</button>

        {generatedQuote && (
          <div className="gen_quote">
            <h1>Generated Quote</h1>
            <blockquote>{generatedQuote}</blockquote>
          </div>
        )}

        <button className="button-29" onClick={handleClick}>
          Regenerate
        </button>
      </div>
    </div>
  );
}

export default Eng_input;
