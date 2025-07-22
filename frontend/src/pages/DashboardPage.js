import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getUserScenarios } from '../services/api';

function DashboardPage() {
    const [scenarios, setScenarios] = useState([]);
    const { token, logout } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchScenarios = async () => {
            try {
                const data = await getUserScenarios(token);
                setScenarios(data);
            } catch (error) {
                console.error("Failed to fetch scenarios:", error);
            }
        };
        if (token) {
            fetchScenarios();
        }
    }, [token]);

    return (
        <div className="container">
            <header className="app-header">
                <h1>Выберите сценарий</h1>
                <div>
                    <button onClick={() => navigate('/admin')} className="admin-button">Панель администратора</button>
                    <button onClick={logout} className="logout-button">Выйти</button>
                </div>
            </header>
            <div className="scenario-list">
                {scenarios.length > 0 ? scenarios.map(scenario => (
                    <div key={scenario.id} className="scenario-card">
                        <h3>{scenario.title}</h3>
                        <p><strong>Цель:</strong> {scenario.goal}</p>
                        <Link to={`/simulation/${scenario.id}`} className="button button-primary">Начать тренировку</Link>
                    </div>
                )) : <p>Сценарии еще не созданы. Зайдите в панель администратора, чтобы добавить первый сценарий.</p>}
            </div>
        </div>
    );
}
export default DashboardPage;
