import React, { useState } from 'react';

function App() {
  const [suggestion, setSuggestion] = useState('');
  const [sceneState, setSceneState] = useState('');
  const [isSceneStarted, setIsSceneStarted] = useState(false);

  const startScene = async () => {
    const response = await fetch('http://localhost:8000/start_scene', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: suggestion }),
    });
    const data = await response.json();
    setSceneState(data.scene_state);
    setIsSceneStarted(true);
  };

  const nextTurn = async () => {
    const response = await fetch('http://localhost:8000/next_turn');
    const data = await response.json();
    setSceneState(data.scene_state);
    if (data.scene_over) {
      setIsSceneStarted(false);
    }
  };

  return (
    <div className="App">
      <h1>Improv App</h1>
      {!isSceneStarted ? (
        <div>
          <input
            type="text"
            value={suggestion}
            onChange={(e) => setSuggestion(e.target.value)}
            placeholder="Enter a suggestion"
          />
          <button onClick={startScene}>Start Scene</button>
        </div>
      ) : (
        <button onClick={nextTurn}>Next Turn</button>
      )}
      <pre>{sceneState}</pre>
    </div>
  );
}

export default App;
