import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './English.css';

function English({ generatedQuote }) {
  const [quote, setQuote] = useState('');
  
  useEffect(() => {
    // Set the quote to the received generatedQuote
    console.log('generatedQuote:', generatedQuote);
    setQuote(generatedQuote);
  }, [generatedQuote]); // Update quote when generatedQuote changes

  const navigate = useNavigate();

  function handleClick(event) {
    navigate('/');
  }


  return (
    <div className='back'>
      <div className="box">
        <h2>Quote of the day</h2>
        <blockquote>{generatedQuote}</blockquote>
        <button className="button-29" role="button" onClick={handleClick}>Regenerate</button>
      </div>
    </div>
  );
}

export default English;