'use client';

import React, { useState, useEffect } from "react";
import Worktable from "./lib/Worktable";
import userPrompt from "./lib/user-prompt";
import CodeDisplay from "./lib/CodeDisplay";
import "./page.css";
// import ForceRefresh from "./lib/forceRefresh";

const App = () => {
  const [code, setCode] = useState("console.log('Hello world')");
  const [error, setError] = useState(false);

  useEffect(() => {
    // Set code to the contents of Worktable file whenever Worktable is updated
    fetch("Worktable.txt")
      .then((res) => res.text())
      .then((text) => setCode(text));
  }, []); // Empty dependency array ensures the effect runs only once

  return (
    <main>
      <div className="header">
        <div className="user-prompt">Prompt: {userPrompt}</div>
      </div>
      <div className="contentPanels">
        <div className="panel">
          <div className="panelHeader">Code</div>
          <CodeDisplay code={code} />
        </div>
        <div className="panel">
          <div className="panelHeader">Output</div>
          {!error && (
            <Worktable
              onComponentError={() => {
                setError(true);
                console.log(error);
              }}
            />
          )}
        </div>
      </div>
    </main>
  );
};

export default App;
