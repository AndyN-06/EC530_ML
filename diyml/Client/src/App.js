import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import LoginPage from './login'
import RegisterPage from './register'
import HomePage from './homepage'
import AppName from './AppName';
import ProjectPage from './projects';
import TestPage from './test'
import ImagePage from './imageupload'
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  // const [creatingUser, setCreatingUser] = useState(false);



  return (
    <Router>
      <div>
        <AppName />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/homepage" element={<HomePage />} />
            <Route path="/project" element={<ProjectPage />} />
            <Route path="/test" element={<TestPage />} />
            <Route path="/image" element={<ImagePage />} />

            <Route path="/" element={<LoginPage />} />
          </Routes>
      </div>
    </Router>
  )

}

export default App;
