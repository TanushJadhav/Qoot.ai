import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";

function Home() {
    const navigate = useNavigate();
    
    function nav_mar(event) {

    navigate('/marathi');
  }

  function nav_eng(event) {

    navigate('/input_eng');
  }

  return (
    <div className="back">
        <div className="box">
        <h2>Choose Language to Generate Quotes</h2>
        
        <div class="button-container">
            <button href="english.html" class="cssbuttons-io-button" onClick={nav_eng} style={{ marginRight: '100px' }}>English
                <div class="icon">
                    <svg
                        height="24"
                        width="24"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path d="M0 0h24v24H0z" fill="none"></path>
                        <path
                            d="M16.172 11l-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
                            fill="currentColor"
                        ></path>
                    </svg>
                </div>
            </button>

            <button class="cssbuttons-io-button" onClick={nav_mar}>Marathi
                <div class="icon">
                    <svg
                        height="24"
                        width="24"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                <path d="M0 0h24v24H0z" fill="none"></path>
                <path
                d="M16.172 11l-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
                fill="currentColor"
                    ></path>
                </svg>
                </div>
            </button>
            </div>
        </div>
    </div>
  );
}

export default Home;