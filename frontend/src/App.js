import React, { useState } from 'react';
import './App.css';

function App() {
  const [suggestion, setSuggestion] = useState('');
  const [sceneState, setSceneState] = useState(null);
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
    console.log('Start scene data:', data);
    setSceneState(data.scene_state);
    setIsSceneStarted(true);
  };

  const nextTurn = async () => {
    const response = await fetch('http://localhost:8000/next_turn');
    const data = await response.json();
    console.log('Next turn data:', data);
    setSceneState(data.scene_state);
    if (data.scene_over) {
      setIsSceneStarted(false);
    }
  };

  const formatAction = (action) => {
    const lines = action.split('\n');
    return lines.map((line, index) => {
      if (line.startsWith('"') && line.endsWith('"')) {
        return <p key={index}>{line}</p>;
      } else if (line.startsWith('*') && line.endsWith('*')) {
        return <p key={index}><i>{line.slice(1, -1)}</i></p>;
      } else {
        return <p key={index}>{line}</p>;
      }
    });
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
      {sceneState && (
        <div className="scene-output">
          <h2>Suggestion: {sceneState.suggestion}</h2>
          <p><strong>Who:</strong> {sceneState.who}</p>
          <p><strong>What:</strong> {sceneState.what}</p>
          <p><strong>Where:</strong> {sceneState.where}</p>
          <p><strong>Problem:</strong> {sceneState.problem}</p>
          <h3>Actions:</h3>
          {sceneState.actions && sceneState.actions.map((turn, index) => (
            <div key={index} className={`turn ${turn.agent.toLowerCase().replace(' ', '-')}`}>
              <h4>{turn.agent}</h4>
              {formatAction(turn.action)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
