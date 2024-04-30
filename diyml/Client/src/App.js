import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [creatingUser, setCreatingUser] = useState(false);

  // to call login function in auth api
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Send post request with username and password
      const response = await axios.post('http://localhost:5000/login', {
        username,
        password,
      });
      alert(JSON.stringify(response.data));
    } catch (error) {
      console.error('Login failed:', error.response ? error.response.data : 'Unknown error');
      alert('Login failed');
    }
  };

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
        setCreatingUser(false); // Switch back to login form after user creation
      }
    } catch (error) {
      console.error('User creation failed:', error.response ? error.response.data : 'Unknown error');
      alert('User creation failed');
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
            <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <input type="email" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <button type="submit">Create User</button>
          </form>
        ) : (
          <form onSubmit={handleLogin}>
            <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
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
