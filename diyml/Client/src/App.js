import React, { useState } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [creatingUser, setCreatingUser] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    // Update the URL to your actual API endpoint for login
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    alert(JSON.stringify(data));
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    // Update the URL to your actual API endpoint for creating a new user
    const response = await fetch('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, email }),
    });
    const data = await response.json();
    alert(JSON.stringify(data));
    if (response.ok) {
      setCreatingUser(false); // Switch back to login form after user creation
    }
  };

  const toggleForm = () => {
    setCreatingUser(!creatingUser);
    setUsername('');
    setPassword('');
    setEmail('');
  };

  return (
    <div className="App">
      <div className="login-container">
        {creatingUser ? (
          <form onSubmit={handleCreateUser}>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <button type="submit">Create User</button>
          </form>
        ) : (
          <form onSubmit={handleLogin}>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button type="submit">Login</button>
          </form>
        )}
        <button onClick={toggleForm}>{creatingUser ? 'Go to Login' : 'Create New User'}</button>
      </div>
    </div>
  );
}

export default App;


// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
