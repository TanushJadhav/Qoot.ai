import React, { createContext, useContext, useState } from 'react';

const QuoteContext = createContext();

export function QuoteProvider({ children }) {
  const [generatedQuote, setGeneratedQuote] = useState('');

  return (
    <QuoteContext.Provider value={{ generatedQuote, setGeneratedQuote }}>
      {children}
    </QuoteContext.Provider>
  );
}

export function useQuote() {
  return useContext(QuoteContext);
}