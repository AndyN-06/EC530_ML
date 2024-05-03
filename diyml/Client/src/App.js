import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import loginPage from './login'
import registerPage from './register'
import homePage from './homepage'
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  // const [creatingUser, setCreatingUser] = useState(false);

  

  return (
    <Router>
      <div>
        <switch>
          
        </switch>
      </div>
    </Router>
  )

  // return (
  //   <div className="App">
  //     <div className="login-container">
  //       {creatingUser ? (
  //         <form onSubmit={handleCreateUser}>
  //           <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
  //           <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
  //           <input type="email" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
  //           <button type="submit">Create User</button>
  //         </form>
  //       ) : (
  //         <form onSubmit={handleLogin}>
  //           <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
  //           <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
  //           <button type="submit">Login</button>
  //         </form>
  //       )}
  //       <button onClick={toggleForm}>{creatingUser ? 'Go to Login' : 'Create New User'}</button>
  //     </div>
  //   </div>
  // );
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
