'use client';

import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const YourComponent = ({ code = `console.log('Hello world')` }) => {
  let x = 36;

  return (
    <>
      <SyntaxHighlighter language="javascript" style={dark}>
        {code}
      </SyntaxHighlighter>
      <div className="x" style={{ opacity: 0 }}>{x}</div>
    </>
  );
};

export default YourComponent;
