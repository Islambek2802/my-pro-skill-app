// frontend/src/App.js (ENGLISH VERSION WITH ANALYSIS)

import React, { useState, useEffect, useRef } from 'react';
import './App.css'; 

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
    // ... (код компонента App остается без изменений) ...
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
                {scenarios.length > 0 ? scenarios.map(scenario => (
                    <div key={scenario.id} className="scenario-card">
                        <h3>{scenario.title}</h3>
                        <p><strong>Goal:</strong> {scenario.goal}</p>
                        <button onClick={() => setCurrentScenario(scenario)} className="button button-primary">
                            Start Training
                        </button>
                    </div>
                )) : <p>Loading scenarios...</p>}
            </div>
        </div>
    );
}

// The simulation component now has analysis logic
function SimulationPage({ scenario, onBack }) {
    const [conversation, setConversation] = useState([{ speaker: 'AI', text: 'Hello! Press the record button and start speaking.' }]);
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [feedback, setFeedback] = useState(null); // State for feedback
    const [isAnalyzing, setIsAnalyzing] = useState(false); // State for analysis process
    const recognitionRef = useRef(null);

    const speakAIResponse = (text) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        window.speechSynthesis.speak(utterance);
    };

    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert('Your browser does not support speech recognition. Please try Google Chrome.');
            return;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.onresult = (event) => {
            const userText = event.results[0][0].transcript;
            handleUserResponse(userText);
        };
        recognition.onend = () => setIsRecording(false);
        recognitionRef.current = recognition;
        speakAIResponse('Hello! Press the record button and start speaking.');
    }, []);


    const handleUserResponse = async (userText) => {
        if (isProcessing) return;
        setIsProcessing(true);
        const updatedConversation = [...conversation, { speaker: 'User', text: userText }];
        setConversation(updatedConversation);
        try {
            const response = await fetch(`${API_BASE_URL}/api/respond`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ conversation: updatedConversation, scenario_id: scenario.id }),
            });
            const data = await response.json();
            setConversation(prev => [...prev, { speaker: 'AI', text: data.ai_response }]);
            speakAIResponse(data.ai_response);
        } catch (error) {
            const errorText = 'Sorry, there was a connection issue.';
            setConversation(prev => [...prev, { speaker: 'AI', text: errorText }]);
            speakAIResponse(errorText);
        } finally {
            setIsProcessing(false);
        }
    };
    
    const handleEndSimulation = async () => {
        setIsAnalyzing(true);
        speakAIResponse("Analyzing your performance. One moment.");
        try {
            const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ conversation, scenario_id: scenario.id }),
            });
            const result = await response.json();
            setFeedback(result);
        } catch (error) {
            alert(`Analysis Error: ${error.message}`);
        } finally {
            setIsAnalyzing(false);
        }
    };

    const toggleRecording = () => {
        if (isRecording) {
            recognitionRef.current.stop();
        } else {
            recognitionRef.current.start();
            setIsRecording(true);
        }
    };

    return (
        <div className="container">
            <header className="app-header">
                <h1>Training: {scenario.title}</h1>
                <button onClick={onBack} className="logout-button">Back to Scenarios</button>
            </header>
            
            <div className="conversation-log">
                {conversation.map((line, index) => <p key={index}><strong>{line.speaker}:</strong> {line.text}</p>)}
            </div>
            
            {!feedback && (
                 <div style={{marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center'}}>
                    <button onClick={toggleRecording} className="button-primary" disabled={isProcessing || isAnalyzing} style={{backgroundColor: isRecording ? '#dc3545' : '#007bff'}}>
                        {isRecording ? 'Stop Recording' : '🎤 Speak'}
                    </button>
                    <button onClick={handleEndSimulation} disabled={isProcessing || isAnalyzing || isRecording}>
                        {isAnalyzing ? 'Analyzing...' : 'End & Analyze'}
                    </button>
                    {isProcessing && <p>AI is thinking...</p>}
                </div>
            )}

            {feedback && (
                <div className="feedback-section">
                    <h2>Performance Review</h2>
                    <p><strong>Goal Achieved:</strong> {feedback.goal_achieved ? '✅ Yes' : '❌ No'}</p>
                    <p><strong>Clarity Score:</strong> {feedback.clarity_score}/10</p>
                    <p><strong>Persuasion Score:</strong> {feedback.persuasion_score}/10</p>
                    <p><strong>Coach's Assessment:</strong> {feedback.overall_assessment}</p>
                </div>
            )}
        </div>
    );
}

export default App;
