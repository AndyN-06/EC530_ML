import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function loginPage(){
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
            
        } catch (error) {
            console.error('Login failed:', error.response ? error.response.data : 'Unknown error');
            alert('Login failed');
        }
    };

    return (

    )
}