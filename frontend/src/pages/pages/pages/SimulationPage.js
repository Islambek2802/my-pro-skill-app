import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { analyzeSimulation } from '../services/api';

function SimulationPage() {
    const { scenarioId } = useParams();
    const navigate = useNavigate();
    const { token } = useAuth();
    const [conversation, setConversation] = useState([{speaker: 'AI', text: 'Здравствуйте! Слушаю вас.'}]);
    const [userInput, setUserInput] = useState('');
    const [feedback, setFeedback] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const chatEndRef = useRef(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [conversation]);

    const handleUserResponse = async (e) => {
        e.preventDefault();
        if (!userInput.trim()) return;

        const updatedConversation = [...conversation, { speaker: 'User', text: userInput }];
        setConversation(updatedConversation);
        setUserInput('');
        
        // В ПРО-версии здесь будет вызов к ИИ для получения ответа клиента
        // А пока добавим простой ответ-заглушку от ИИ
        setTimeout(() => {
            setConversation(prev => [...prev, {speaker: 'AI', text: 'Хорошо, я вас понял. Что вы предлагаете?'}]);
        }, 1000);
    };

    const handleEndSimulation = async () => {
        setIsAnalyzing(true);
        try {
            const result = await analyzeSimulation(conversation, scenarioId, token);
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
                <h1>Симуляция диалога</h1>
                <button onClick={() => navigate('/')} className="logout-button">Завершить и вернуться</button>
            </header>
            
            <div className="conversation-log">
                {conversation.map((line, index) => (
                    <p key={index}><strong>{line.speaker}:</strong> {line.text}</p>
                ))}
                <div ref={chatEndRef} />
            </div>

            {!feedback && (
                <form onSubmit={handleUserResponse}>
                    <div style={{display: 'flex', gap: '1rem'}}>
                        <input
                            type="text"
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            placeholder="Ваш ответ..."
                            style={{flexGrow: 1, padding: '12px', border: '1px solid #ced4da', borderRadius: '8px'}}
                            disabled={isAnalyzing}
                        />
                        <button type="submit" className="button-primary" disabled={isAnalyzing}>Отправить</button>
                    </div>
                </form>
            )}

            {!feedback && (
                <button onClick={handleEndSimulation} disabled={isAnalyzing} style={{marginTop: '1rem'}}>
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

export default SimulationPage;
