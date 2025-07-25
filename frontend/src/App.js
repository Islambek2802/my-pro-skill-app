// frontend/src/App.js (УПРОЩЕННАЯ ВЕРСИЯ)

import React, { useState, useEffect } from 'react';
import './App.css'; // Подключаем стили

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
    const [scenarios, setScenarios] = useState([]);
    const [currentScenario, setCurrentScenario] = useState(null);

    // Загружаем сценарии при запуске приложения
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
        // Если выбран сценарий, показываем экран симуляции
        return <SimulationPage scenario={currentScenario} onBack={() => setCurrentScenario(null)} />;
    }

    // Если сценарий не выбран, показываем список сценариев
    return (
        <div className="container">
            <header className="app-header">
                <h1>Выберите сценарий для тренировки</h1>
            </header>
            <div className="scenario-list">
                {scenarios.length > 0 ? scenarios.map(scenario => (
                    <div key={scenario.id} className="scenario-card">
                        <h3>{scenario.title}</h3>
                        <p><strong>Цель:</strong> {scenario.goal}</p>
                        <button onClick={() => setCurrentScenario(scenario)} className="button button-primary">
                            Начать тренировку
                        </button>
                    </div>
                )) : <p>Загрузка сценариев...</p>}
            </div>
        </div>
    );
}


// Компонент симуляции, теперь находится прямо здесь
function SimulationPage({ scenario, onBack }) {
    const [conversation, setConversation] = useState([{ speaker: 'AI', text: 'Здравствуйте! Слушаю вас.' }]);
    const [userInput, setUserInput] = useState('');
    const [feedback, setFeedback] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    const handleUserResponse = (e) => {
        e.preventDefault();
        if (!userInput.trim()) return;

        const updatedConversation = [...conversation, { speaker: 'User', text: userInput }];
        setConversation(updatedConversation);
        setUserInput('');

        setTimeout(() => {
            setConversation(prev => [...prev, { speaker: 'AI', text: 'Интересно, расскажите подробнее.' }]);
        }, 1000);
    };

    const handleEndSimulation = async () => {
        setIsAnalyzing(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ conversation, scenario_id: scenario.id }),
            });
            const result = await response.json();
            setFeedback(result);
        } catch (error) {
            alert(`Ошибка анализа: ${error.message}`);
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="container">
            <header className="app-header">
                <h1>Тренировка: {scenario.title}</h1>
                <button onClick={onBack} className="logout-button">Вернуться к сценариям</button>
            </header>
            
            <div className="conversation-log">
                {conversation.map((line, index) => (
                    <p key={index}><strong>{line.speaker}:</strong> {line.text}</p>
                ))}
            </div>

            {!feedback && (
                <form onSubmit={handleUserResponse}>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <input
                            type="text"
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            placeholder="Ваш ответ..."
                            style={{ flexGrow: 1, padding: '12px', border: '1px solid #ced4da', borderRadius: '8px' }}
                            disabled={isAnalyzing}
                        />
                        <button type="submit" className="button-primary" disabled={isAnalyzing}>Отправить</button>
                    </div>
                </form>
            )}

            {!feedback && (
                <button onClick={handleEndSimulation} disabled={isAnalyzing} style={{ marginTop: '1rem' }}>
                    {isAnalyzing ? 'Анализирую...' : 'Завершить и проанализировать'}
                </button>
            )}

            {feedback && (
                <div className="feedback-section">
                    <h2>Результаты анализа</h2>
                    <p><strong>Цель достигнута:</strong> {feedback.goal_achieved ? '✅ Да' : '❌ Нет'}</p>
                    <p><strong>Использованные ключевые слова:</strong></p>
                    <ul>
                        {feedback.keywords_usage?.map((kw, i) => <li key={i}>{kw}</li>)}
                    </ul>
                    <p><strong>Комментарий по достижению цели:</strong> {feedback.feedback_on_goal}</p>
                    <p><strong>Общая оценка:</strong> {feedback.overall_assessment}</p>
                </div>
            )}
        </div>
    );
}

export default App;
