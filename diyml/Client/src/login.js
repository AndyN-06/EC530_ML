import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginPage(){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            // Send post request with username and password
            const response = await axios.post('http://localhost:5000/login', {
                username,
                password,
            });
            alert(JSON.stringify(response.data));
            // navigate to homepage
            navigate('/homepage');
        } catch (error) {
            console.error('Login failed:', error.response ? error.response.data : 'Unknown error');
            alert('Login failed');
        }
    };

    const handleGoToRegister = () => {
        navigate('/register');
    };

    const handleGoToHome = () => {
        navigate('/homepage');
    };

    const handleGoToProject = () => {
        navigate('/project');
    };

    const handleGoToImage = () => {
        navigate('/image');
    }

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
                <button type="button" className="btn-register" onClick={handleGoToRegister}>
                    Create New User
                </button>
                <button type="submit" className="btn-login">Login</button>
            </form>
            <button type="button" className="btn-register" onClick={handleGoToHome}>
                Go to homepage
            </button>
            <button type="button" className="btn-register" onClick={handleGoToProject}>
                Go to project page
            </button>
            <button type="button" className="btn-register" onClick={handleGoToImage}>
                Go to image page
            </button>
        </div>
    );
}

export default LoginPage;