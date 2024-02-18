'use client';

import React, { useState, useEffect } from "react";
import Worktable from "./lib/Worktable";
import userPrompt from "./lib/user-prompt";
import CodeDisplay from "./lib/CodeDisplay";
import "./page.css";

const App = () => {
  const [code, setCode] = useState("console.log('Hello world')");
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("Worktable.txt")
      .then((res) => res.text())
      .then((text) => setCode(text));
  }, []);

  return (
    <main>
      <div className="header">
        <div className="user-prompt">Prompt: {userPrompt}</div>
      </div>
      
      <div className="contentPanels">
        <div className="panel">
          <div className="panelHeader">Code</div>
          <div className="code">
            <CodeDisplay code={code} />
          </div>
        </div>
        <div className="panel">
          <div className="panelHeader">Output</div>
          <div className="component">
            <ErrorBoundary>
              {!error && <Worktable onError={() => setError(true)} />}
              {error && <div class="error-container">
                <div class="error-text">Error in generation</div>
              </div>}
            </ErrorBoundary>
          </div>
        </div>
      </div>
      <div className="fixed bottom-0 right-0 p-2 bg-gray-800 text-white text-sm rounded-tl-md text-2xl">
        <div>Keyphrases:</div>
          <ul>
            <li>Delete all</li>
            <li>Fix error</li>
          </ul>
      </div>
    </main>
  );
};

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <div class="w-full h-full flex justify-center items-center">
      <div class="text-4xl">Error in generation ☹️</div>
    </div>;
    }
    return this.props.children;
  }
}

export default App;
