import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { loginUser, registerUser } from '../services/api';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            if (isRegistering) {
                await registerUser(username, password);
                alert('Регистрация прошла успешно! Теперь вы можете войти.');
                setIsRegistering(false);
            } else {
                const data = await loginUser(username, password);
                login(data.access_token);
                navigate('/');
            }
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="auth-container">
            <div className="container auth-form">
                <form onSubmit={handleSubmit}>
                    <h2>{isRegistering ? 'Регистрация' : 'Вход в систему'}</h2>
                    {error && <p style={{color: 'red'}}>{error}</p>}
                    <div className="form-group">
                        <label htmlFor="username">Имя пользователя</label>
                        <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Пароль</label>
                        <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    <button type="submit" className='button-primary'>{isRegistering ? 'Зарегистрироваться' : 'Войти'}</button>
                    <p style={{textAlign: 'center', marginTop: '1rem'}}>
                        {isRegistering ? 'Уже есть аккаунт? ' : 'Нет аккаунта? '}
                        <span onClick={() => setIsRegistering(!isRegistering)} style={{color: '#007bff', cursor: 'pointer'}}>
                            {isRegistering ? 'Войти' : 'Зарегистрироваться'}
                        </span>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default LoginPage;
