import React from 'react';
import { useNavigate } from 'react-router-dom';

function AppName() {
    const navigate = useNavigate();

    return (
        <header style={{ backgroundColor: '#f4f4f4', padding: '10px 20px' }}>
            <h1 style={{ cursor: 'pointer' }} onClick={() => navigate('/')}>
                Identifier App
            </h1>
        </header>
    );
}

export default AppName;
