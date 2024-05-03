import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function registerPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

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
            
            }
        } catch (error) {
            console.error('User creation failed:', error.response ? error.response.data : 'Unknown error');
            alert('User creation failed');
        }
    };

    return (

    )

}