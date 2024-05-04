import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const navigate = useNavigate();

    // to call new_user function in auth api
    const handleCreateUser = async (e) => {
        e.preventDefault();
        try {
            // send post request with username password and email
            const response = await axios.post('http://localhost:5000/users', {
                username,
                password,
                email,
            });
            alert(JSON.stringify(response.data));
            if (response.status === 200 || response.status === 201) {
                // navigate to login page
                navigate('/login');
            }
        } catch (error) {
            console.error('User creation failed:', error.response ? error.response.data : 'Unknown error');
            alert('User creation failed');
        }
    };

    const handleGoToLogin = () => {
        navigate('/login');
    };

    return (
        <div className="register-container">
            <h2>Sign Up</h2>
            <form onSubmit={handleCreateUser}>
                <label htmlFor="username">Username</label>
                <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <button type="submit" className="btn-signup">Sign Up</button>
                <button type="button" className="btn-back-to-login" onClick={handleGoToLogin}>
                    Back to Login
                </button>
            </form>
        </div>
    );
}

export default RegisterPage;