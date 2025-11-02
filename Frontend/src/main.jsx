import React from 'react'
import ReactDOM from 'react-dom/client'
import SeatServeMVP from './SeatServeMVP.jsx'
import Auth from './Auth.jsx'
import './index.css'

function App() {
  const isLoggedIn = localStorage.getItem('seatserve_logged_in') === 'true';
  
  if (!isLoggedIn) {
    return <Auth />;
  }
  
  return <SeatServeMVP />;
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
