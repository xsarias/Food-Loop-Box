import { FaHandPaper } from "react-icons/fa";
import { FaHandHoldingHeart } from "react-icons/fa";
import { MdSell } from "react-icons/md";
import { FiBox } from "react-icons/fi";
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import "./Home.css"

function Home() {
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuth()

  const handleLogout = async () => {
    await logout()
  }

  return (
    <div className="home-page">
      <header className="home-header">
        <div className="brand-block">
          <div className="brand-icon-home">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Red local contra el desperdicio</p>
          </div>
        </div>

        {isAuthenticated ? (
          <div className="user-block">
            <span className="user-greeting">
              Hola, <strong>{user.first_name || user.username}</strong>
            </span>
            <button className="login-btn" type="button" onClick={handleLogout}>
              Cerrar sesión
            </button>
          </div>
        ) : (
          <div className="user-block">
            <button
              className="login-btn"
              type="button"
              onClick={() => navigate('/login')}
            >
              Iniciar sesión
            </button>
            <button
              className="register-btn"
              type="button"
              onClick={() => navigate('/register')}
            >
              Registrarse
            </button>
          </div>
        )}
      </header>

      <main className="home-main">
        <section className="hero-card">
          <div className="hero-icon">FLB</div>
          <h1>Food Loop Box</h1>
          <p>Lo que sobra, alimenta. Dona, comparte, recupera y mueve alimentos en tu comunidad.</p>
        </section>

        <section className="actions-card">
          <h3>¿Qué deseas hacer hoy?</h3>
          <div className="actions-grid">
            <button className="boton1" onClick={() => navigate('/obtener')}>
              <FaHandPaper /> Obtener Alimento
            </button>
            <button className="boton2" onClick={() => navigate('/donar')}>
              <FaHandHoldingHeart /> Donar Alimento
            </button>
            <button className="boton1" onClick={() => navigate('/vender')}>
              <MdSell /> Vender Alimento
            </button>
            <button className="boton2" onClick={() => navigate('/reclamar')}>
              <FiBox /> Reclamar Alimento
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}

export default Home
