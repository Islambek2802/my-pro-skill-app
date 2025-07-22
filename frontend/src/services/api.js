// frontend/src/services/api.js

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const callApi = async (endpoint, token, method = 'GET', body = null) => {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
    };
    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'API call failed');
    }
    // Если тело ответа пустое, вернем null
    const responseText = await response.text();
    return responseText ? JSON.parse(responseText) : null;
};

// Auth
export const loginUser = async (username, password) => {
    const formBody = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
    const response = await fetch(`${API_BASE_URL}/api/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formBody,
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Login failed');
    }
    return response.json();
};

export const registerUser = (username, password) => callApi('/api/auth/register', null, 'POST', { username, password });

// Scenarios (Admin)
export const createScenario = (scenarioData, token) => callApi('/api/admin/scenarios', token, 'POST', scenarioData);
export const getAdminScenarios = (token) => callApi('/api/admin/scenarios', token);

// App (User)
export const getUserScenarios = (token) => callApi('/api/app/simulation/scenarios', token);
export const analyzeSimulation = (conversation, scenario_id, token) => callApi('/api/app/simulation/analyze', token, 'POST', { conversation, scenario_id });
