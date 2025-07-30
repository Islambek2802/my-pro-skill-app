// frontend/src/App.js (ВЕРСИЯ С НЕПРЕРЫВНОЙ ЗАПИСЬЮ И КАЧЕСТВЕННЫМ ГОЛОСОМ)

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
                {scenarios.map(scenario => (
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

function SimulationPage({ scenario, onBack }) {
    const [conversation, setConversation] = useState([{ speaker: 'AI', text: 'Hello! Press the record button to start.' }]);
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const recognitionRef = useRef(null);

    // НОВАЯ ФУНКЦИЯ ОЗВУЧИВАНИЯ ЧЕРЕЗ БЭКЕНД
    const speakAIResponse = async (text) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/synthesize-speech`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text }),
            });
            if (!response.ok) throw new Error("Failed to fetch audio");

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
        } catch (error) {
            console.error("Audio playback error:", error);
        }
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
        recognition.continuous = true; // <-- ВКЛЮЧАЕМ РЕЖИМ НЕПРЕРЫВНОЙ ЗАПИСИ

        recognition.onresult = (event) => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            if (finalTranscript) {
                handleUserResponse(finalTranscript.trim());
            }
        };
        
        recognitionRef.current = recognition;
        speakAIResponse('Hello! Press the record button to start.');
    }, []);


    const handleUserResponse = async (userText) => {
        recognitionRef.current.stop(); // Останавливаем запись, когда пользователь закончил говорить
        setIsRecording(false);
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
            await speakAIResponse(data.ai_response);
        } catch (error) {
            console.error("Failed to get AI response:", error);
            const errorText = 'Sorry, there was a connection issue.';
            setConversation(prev => [...prev, { speaker: 'AI', text: errorText }]);
            await speakAIResponse(errorText);
        } finally {
            setIsProcessing(false);
        }
    };

    const toggleRecording = () => {
        if (isRecording) {
            recognitionRef.current.stop();
            setIsRecording(false);
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

            <div style={{marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center'}}>
                <button onClick={toggleRecording} className="button-primary" disabled={isProcessing} style={{backgroundColor: isRecording ? '#dc3545' : '#007bff'}}>
                    {isRecording ? '■ Stop' : '🎤 Speak'}
                </button>
                {isRecording && <p>Listening...</p>}
                {isProcessing && <p>AI is thinking...</p>}
            </div>
        </div>
    );
}

export default App;
