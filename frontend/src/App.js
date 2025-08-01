import React, { useState, useEffect } from 'react';
import './App.css'; 

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
    const [scenarios, setScenarios] = useState([]);
    const [currentScenario, setCurrentScenario] = useState(null);

    useEffect(() => {
        const fetchScenarios = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/scenarios`);
                const data = await response.json();
                setScenarios(data);
            } catch (error) {
                console.error("Failed to fetch scenarios:", error);
            }
        };
        fetchScenarios();
    }, []);

    if (currentScenario) {
        return <SimulationPage scenario={currentScenario} onBack={() => setCurrentScenario(null)} />;
    }

    return (
        <div className="container">
            <header className="app-header">
                <h1>Choose a Scenario to Practice</h1>
            </header>
            <div className="scenario-list">
                {scenarios.length > 0 ? (
                    scenarios.map(scenario => (
                        <div key={scenario.id} className="scenario-card">
                            <h3>{scenario.title}</h3>
                            <p><strong>Goal:</strong> {scenario.goal}</p>
                            <button onClick={() => setCurrentScenario(scenario)} className="button button-primary">
                                Start Training
                            </button>
                        </div>
                    ))
                ) : (
                    <p>Loading scenarios...</p>
                )}
            </div>
        </div>
    );
}


// ...The rest of your SimulationPage component goes here...
function SimulationPage({ scenario, onBack }) {
    // (This part of the code remains the same as the last version I sent)
    // ...
}

export default App;
