import { useState } from 'react';


const Component = () => {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState(true);

  const handleClick = (index) => {
    if (board[index] || calculateWinner(board) || calculeteDraw(board)) return;

    const newBoard = [...board];
    newBoard[index] = xIsNext ? 'X' : 'O';
    setBoard(newBoard);
    setXIsNext(!xIsNext);
  };

  const calculateWinner = (squares) => {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6]
    ];
    for (const line of lines) {
      if (calculateLineWin(line, squares)) return line;
    }
    return null;
  };

  const calculateLineWin = (line, squares) => {
    const [a, b, c] = line;
    return squares[a] && squares[a] === squares[b] && squares[b] === squares[c];
  };

  const calculeteDraw = (squares) => {
    return squares.every((square) => square !== null);
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="border bg-gray-300 p-5 rounded shadow-lg">
        <h1 className="text-xl text-center mb-5">Tic Tac Toe</h1>
        <div className="grid grid-cols-3 gap-2">
          {board.map((square, index) => (
            <button
              key={index}
              className="bg-gray-400 text-white p-1 rounded"
              onClick={() => handleClick(index)}
              disabled={square !== null}
            >
              {square}
            </button>
          ))}
        </div>
        <p className="text-center text-xl mt-5">{calculateWinner(board) ? `Winner: ${calculateWinner(board).map((el, i) => board[i + 3 * Math.floor(i / 3)]).join('')}` : calculeteDraw(board) && 'It\'s a draw'}</p>
        <p className="text-center text-xl mt-5">{xIsNext ? 'X' : 'O'} turn</p>
      </div>
    </div>
  );
};

export default Component;
