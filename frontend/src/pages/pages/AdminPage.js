import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { createScenario, getAdminScenarios } from '../services/api';

function AdminPage() {
    const [title, setTitle] = useState('');
    const [goal, setGoal] = useState('');
    const [persona, setPersona] = useState('');
    const [keywords, setKeywords] = useState('');
    const [scenarios, setScenarios] = useState([]);
    const { token } = useAuth();
    const navigate = useNavigate();

    const fetchScenarios = async () => {
        try {
            const data = await getAdminScenarios(token);
            setScenarios(data);
        } catch (error) {
            console.error("Failed to fetch scenarios:", error);
        }
    };

    useEffect(() => {
        if(token) fetchScenarios();
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const scenarioData = {
            title,
            goal,
            customer_persona: persona,
            required_keywords: keywords.split(',').map(k => k.trim()),
        };
        try {
            await createScenario(scenarioData, token);
            alert('Сценарий успешно создан!');
            setTitle(''); setGoal(''); setPersona(''); setKeywords('');
            fetchScenarios();
        } catch (error) {
            alert(`Ошибка при создании сценария: ${error.message}`);
        }
    };

    return (
        <div className="container">
            <header className="app-header">
                <h1>Панель администратора</h1>
                <button onClick={() => navigate('/')} className="logout-button">На главную</button>
            </header>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem'}}>
                <div>
                    <h2>Создать новый сценарий</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Название</label>
                            <input type="text" value={title} onChange={e => setTitle(e.target.value)} required />
                        </div>
                        <div className="form-group">
                            <label>Цель звонка для сотрудника</label>
                            <input type="text" value={goal} onChange={e => setGoal(e.target.value)} required />
                        </div>
                        <div className="form-group">
                            <label>Описание клиента (для ИИ)</label>
                            <textarea value={persona} onChange={e => setPersona(e.target.value)} required style={{width: '100%', minHeight: '80px', padding: '12px', border: '1px solid #ced4da', borderRadius: '8px', fontSize: '1rem'}}></textarea>
                        </div>
                        <div className="form-group">
                            <label>Ключевые слова (через запятую)</label>
                            <input type="text" value={keywords} onChange={e => setKeywords(e.target.value)} required />
                        </div>
                        <button type="submit" className="button-primary">Создать сценарий</button>
                    </form>
                </div>
                <div>
                    <h2>Существующие сценарии</h2>
                    <div className="scenario-list">
                        {scenarios.map(s => (
                            <div key={s.id} className="scenario-card" style={{borderColor: '#ccc'}}>
                                <h3>{s.title}</h3>
                                <p><strong>Цель:</strong> {s.goal}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
export default AdminPage;
