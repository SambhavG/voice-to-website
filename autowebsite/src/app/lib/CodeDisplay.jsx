'use client';

import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const YourComponent = ({ code = `console.log('Hello world')` }) => {
let x = 1708263410;

  return (
    <>
      <SyntaxHighlighter language="javascript" style={atomDark}>
        {code}
      </SyntaxHighlighter>
      <div className="x" style={{ opacity: 0 }}>{x}</div>
    </>
  );
};

export default YourComponent;
